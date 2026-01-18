"""Config flow for Ever Powerline UPS integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DEFAULT_PORT, DEFAULT_SLAVE_ID, DOMAIN, REG_IDENTIFIERS

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
    }
)


class EverPowerlineUPSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ever Powerline UPS."""

    VERSION = 1

    async def _test_connection(
        self, host: str, port: int
    ) -> tuple[bool, str | None, str | None]:
        """Test connection to the UPS and return (success, model, serial)."""
        client = AsyncModbusTcpClient(host=host, port=port, timeout=10)
        
        try:
            connected = await client.connect()
            if not connected:
                return False, None, None

            # Read identifiers to verify connection
            result = await client.read_holding_registers(
                REG_IDENTIFIERS, 80, slave=DEFAULT_SLAVE_ID
            )
            
            if result.isError():
                return False, None, None

            # Decode model and serial
            regs = result.registers
            
            def decode_string(registers: list[int], max_chars: int) -> str:
                chars = []
                for reg in registers:
                    high_byte = (reg >> 8) & 0xFF
                    low_byte = reg & 0xFF
                    if 0x20 <= high_byte <= 0x7A:
                        chars.append(chr(high_byte))
                    if 0x20 <= low_byte <= 0x7A:
                        chars.append(chr(low_byte))
                return "".join(chars).strip("\x00").strip()[:max_chars]

            model = decode_string(regs[16:48], 63)
            serial = decode_string(regs[56:64], 15)
            
            return True, model, serial

        except ModbusException as err:
            _LOGGER.error("Modbus error during connection test: %s", err)
            return False, None, None
        except Exception as err:
            _LOGGER.error("Error during connection test: %s", err)
            return False, None, None
        finally:
            client.close()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            success, model, serial = await self._test_connection(host, port)

            if success:
                # Use serial number as unique ID, fallback to host
                unique_id = serial or host
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                title = f"Ever {model}" if model else f"Ever UPS ({host})"
                
                return self.async_create_entry(
                    title=title,
                    data=user_input,
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
