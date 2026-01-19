"""DataUpdateCoordinator for Ever Powerline UPS."""

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE_ID,
    DOMAIN,
    REG_IDENTIFIERS,
    REG_MEASUREMENTS,
    REG_RATED,
    REG_STATUS,
    REG_WARNINGS,
    OPERATING_MODE_NAMES,
    BATTERY_STATUS_NAMES,
    BATTERY_TEST_RESULT_NAMES,
    ABM_STATUS_NAMES,
    OperatingMode,
    BatteryStatus,
    BatteryTestResult,
    ABMStatus,
)

_LOGGER = logging.getLogger(__name__)


class EverUPSCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for Ever Powerline UPS data."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.host = host
        self.port = port
        self._client: AsyncModbusTcpClient | None = None
        self._lock = asyncio.Lock()

        # Device info (fetched once)
        self.manufacturer: str = "EVER"
        self.model: str = ""
        self.firmware_version: str = ""
        self.serial_number: str = ""

        # Rated data (fetched once)
        self.rated_apparent_power: int = 0
        self.rated_active_power: int = 0
        self.rated_battery_voltage: float = 0.0
        self.rated_output_voltage: float = 0.0
        self.rated_output_frequency: float = 0.0

        self._device_info_fetched = False

    async def _ensure_connected(self) -> AsyncModbusTcpClient:
        """Ensure we have a connected client."""
        if self._client is None or not self._client.connected:
            self._client = AsyncModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=10,
            )
            connected = await self._client.connect()
            if not connected:
                raise UpdateFailed(f"Failed to connect to {self.host}:{self.port}")
        return self._client

    async def async_close(self) -> None:
        """Close the Modbus connection."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def _decode_string(self, registers: list[int], max_chars: int) -> str:
        """Decode ASCII string from Modbus registers."""
        chars = []
        for reg in registers:
            high_byte = (reg >> 8) & 0xFF
            low_byte = reg & 0xFF
            if 0x20 <= high_byte <= 0x7A:
                chars.append(chr(high_byte))
            if 0x20 <= low_byte <= 0x7A:
                chars.append(chr(low_byte))
        return "".join(chars).strip("\x00").strip()[:max_chars]

    async def _fetch_device_info(self, client: AsyncModbusTcpClient) -> None:
        """Fetch device identification (only once)."""
        if self._device_info_fetched:
            return

        try:
            # Read identifiers (0x0000, 80 words)
            result = await client.read_holding_registers(
                REG_IDENTIFIERS, count=80, device_id=DEFAULT_SLAVE_ID
            )
            if result.isError():
                _LOGGER.warning("Failed to read device identifiers")
                return

            regs = result.registers
            self.manufacturer = self._decode_string(regs[0:16], 31) or "EVER"
            self.model = self._decode_string(regs[16:48], 63)
            self.firmware_version = self._decode_string(regs[48:56], 15)
            self.serial_number = self._decode_string(regs[56:64], 15)

            # Read rated data (0x00E0, 16 words)
            result = await client.read_holding_registers(
                REG_RATED, count=16, device_id=DEFAULT_SLAVE_ID
            )
            if not result.isError():
                regs = result.registers
                self.rated_apparent_power = regs[1] * 100  # VA
                self.rated_battery_voltage = regs[2] / 10.0  # V
                self.rated_output_voltage = regs[4] / 10.0  # V
                self.rated_output_frequency = regs[5] / 10.0  # Hz
                self.rated_active_power = regs[6] * 100  # W

            self._device_info_fetched = True
            _LOGGER.debug(
                "Device info: %s %s (FW: %s, SN: %s)",
                self.manufacturer,
                self.model,
                self.firmware_version,
                self.serial_number,
            )
        except ModbusException as err:
            _LOGGER.warning("Error fetching device info: %s", err)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the UPS."""
        async with self._lock:
            try:
                client = await self._ensure_connected()

                # Fetch device info once
                await self._fetch_device_info(client)

                data: dict[str, Any] = {}

                # Read warnings (0x0060, 6 words)
                result = await client.read_holding_registers(
                    REG_WARNINGS, count=6, device_id=DEFAULT_SLAVE_ID
                )
                if result.isError():
                    raise UpdateFailed("Failed to read warning registers")

                warnings = result.registers
                data["warnings_0"] = warnings[0]
                data["warnings_1"] = warnings[1]
                data["warnings_2"] = warnings[2]

                # Read status (0x0070, 10 words)
                result = await client.read_holding_registers(
                    REG_STATUS, count=10, device_id=DEFAULT_SLAVE_ID
                )
                if result.isError():
                    raise UpdateFailed("Failed to read status registers")

                status = result.registers
                ups_type = (status[0] >> 8) & 0xFF
                operating_mode = status[0] & 0xFF
                input_phases = (status[1] >> 8) & 0xFF
                output_phases = status[1] & 0xFF
                battery_status = (status[2] >> 8) & 0xFF
                test_result = status[2] & 0xFF
                input_source = (status[3] >> 8) & 0xFF
                bypass_phases = status[3] & 0xFF
                abm_status = status[4] & 0xFF

                data["ups_type"] = ups_type
                data["operating_mode"] = operating_mode
                data["operating_mode_name"] = OPERATING_MODE_NAMES.get(
                    operating_mode, f"Unknown ({operating_mode})"
                )
                data["input_phases"] = input_phases
                data["output_phases"] = output_phases
                data["battery_status"] = battery_status
                data["battery_status_name"] = BATTERY_STATUS_NAMES.get(
                    battery_status, f"Unknown ({battery_status})"
                )
                data["test_result"] = test_result
                data["test_result_name"] = BATTERY_TEST_RESULT_NAMES.get(
                    test_result, f"Unknown ({test_result})"
                )
                data["input_source"] = input_source
                data["bypass_phases"] = bypass_phases
                data["abm_status"] = abm_status
                data["abm_status_name"] = ABM_STATUS_NAMES.get(
                    abm_status, f"Unknown ({abm_status})"
                )

                # Read measurements (0x0080, 80 words)
                result = await client.read_holding_registers(
                    REG_MEASUREMENTS, count=80, device_id=DEFAULT_SLAVE_ID
                )
                if result.isError():
                    raise UpdateFailed("Failed to read measurement registers")

                meas = result.registers
                data["temperature"] = meas[0] / 10.0  # C
                data["input_frequency"] = meas[1] / 10.0  # Hz
                data["input_voltage_l1"] = meas[4] / 10.0  # V
                data["input_voltage_l2"] = meas[5] / 10.0  # V
                data["input_voltage_l3"] = meas[6] / 10.0  # V
                data["output_voltage_l1"] = meas[19] / 10.0  # V (0x0093 - 0x0080 = 19)
                data["output_voltage_l2"] = meas[20] / 10.0  # V
                data["output_voltage_l3"] = meas[21] / 10.0  # V
                data["output_current_l1"] = meas[25] / 10.0  # A (0x0099 - 0x0080 = 25)
                data["output_current_l2"] = meas[26] / 10.0  # A
                data["output_current_l3"] = meas[27] / 10.0  # A
                data["active_power_l1"] = meas[28] * 100  # W (0x009C - 0x0080 = 28)
                data["active_power_l2"] = meas[29] * 100  # W
                data["active_power_l3"] = meas[30] * 100  # W
                data["apparent_power_l1"] = meas[31] * 100  # VA (0x009F - 0x0080 = 31)
                data["apparent_power_l2"] = meas[32] * 100  # VA
                data["apparent_power_l3"] = meas[33] * 100  # VA
                # Load values - 0xFFFF (65535) means "not available" for unused phases
                data["load_l1"] = meas[34] if meas[34] != 0xFFFF else None
                data["load_l2"] = meas[35] if meas[35] != 0xFFFF else None
                data["load_l3"] = meas[36] if meas[36] != 0xFFFF else None
                data["runtime_minutes"] = meas[37]  # min (0x00A5 - 0x0080 = 37)
                data["runtime_seconds"] = meas[38]  # sec
                data["runtime_remaining"] = meas[37] + (meas[38] / 60.0)  # total min
                data["battery_charge"] = meas[41]  # % (0x00A9 - 0x0080 = 41)
                data["battery_voltage_pos"] = meas[42] / 10.0  # V (0x00AA)
                data["battery_voltage_neg"] = meas[43] / 10.0  # V (0x00AB)
                data["battery_voltage"] = (meas[42] + meas[43]) / 10.0  # V total
                data["bypass_frequency"] = meas[45] / 10.0  # Hz (0x00AD - 0x0080 = 45)
                data["bypass_voltage"] = meas[48] / 10.0  # V (0x00B0 - 0x0080 = 48)

                # Calculate totals for single-phase display
                data["active_power_total"] = (
                    data["active_power_l1"]
                    + data["active_power_l2"]
                    + data["active_power_l3"]
                )
                data["apparent_power_total"] = (
                    data["apparent_power_l1"]
                    + data["apparent_power_l2"]
                    + data["apparent_power_l3"]
                )
                # Calculate load_total from valid phases only (ignore None values)
                valid_loads = [
                    v
                    for v in [data["load_l1"], data["load_l2"], data["load_l3"]]
                    if v is not None
                ]
                data["load_total"] = max(valid_loads) if valid_loads else None

                return data

            except ModbusException as err:
                self._client = None
                raise UpdateFailed(f"Modbus error: {err}") from err
            except Exception as err:
                self._client = None
                raise UpdateFailed(f"Error communicating with UPS: {err}") from err

    async def async_write_register(self, address: int, value: int) -> bool:
        """Write a single register to UPS."""
        async with self._lock:
            try:
                client = await self._ensure_connected()
                result = await client.write_register(
                    address, value, device_id=DEFAULT_SLAVE_ID
                )
                if result.isError():
                    _LOGGER.error(
                        "Failed to write register 0x%04X: %s", address, result
                    )
                    return False
                return True
            except ModbusException as err:
                _LOGGER.error("Modbus error writing register: %s", err)
                return False

    async def async_write_registers(self, address: int, values: list[int]) -> bool:
        """Write multiple registers to UPS."""
        async with self._lock:
            try:
                client = await self._ensure_connected()
                result = await client.write_registers(
                    address, values, device_id=DEFAULT_SLAVE_ID
                )
                if result.isError():
                    _LOGGER.error(
                        "Failed to write register 0x%04X: %s", address, result
                    )
                    return False
                return True
            except ModbusException as err:
                _LOGGER.error("Modbus error writing register: %s", err)
                return False

    async def async_read_registers(self, address: int, count: int) -> list[int] | None:
        """Read registers from the UPS."""
        async with self._lock:
            try:
                client = await self._ensure_connected()
                result = await client.read_holding_registers(
                    address, count=count, device_id=DEFAULT_SLAVE_ID
                )
                if result.isError():
                    _LOGGER.error(
                        "Failed to read registers 0x%04X: %s", address, result
                    )
                    return None
                return result.registers
            except ModbusException as err:
                _LOGGER.error("Modbus error reading registers: %s", err)
                return None

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info for the UPS."""
        return {
            "identifiers": {(DOMAIN, self.serial_number or self.host)},
            "name": f"Ever {self.model}" if self.model else "Ever Powerline UPS",
            "manufacturer": self.manufacturer,
            "model": self.model,
            "sw_version": self.firmware_version,
            "serial_number": self.serial_number,
        }
