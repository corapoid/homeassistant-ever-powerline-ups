"""Number platform for Ever Powerline UPS."""
from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    REG_SHUTDOWN_DELAY_MSB,
    REG_STARTUP_DELAY_MSB,
)
from .coordinator import EverUPSCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EverUPSNumberEntityDescription(NumberEntityDescription):
    """Describes Ever UPS number entity."""

    register_address: int


NUMBER_DESCRIPTIONS: tuple[EverUPSNumberEntityDescription, ...] = (
    EverUPSNumberEntityDescription(
        key="shutdown_delay",
        translation_key="shutdown_delay",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=NumberDeviceClass.DURATION,
        native_min_value=0,
        native_max_value=65535,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:timer-off-outline",
        register_address=REG_SHUTDOWN_DELAY_MSB,
    ),
    EverUPSNumberEntityDescription(
        key="startup_delay",
        translation_key="startup_delay",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=NumberDeviceClass.DURATION,
        native_min_value=0,
        native_max_value=65535,
        native_step=1,
        mode=NumberMode.BOX,
        icon="mdi:timer-outline",
        register_address=REG_STARTUP_DELAY_MSB,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ever UPS numbers based on a config entry."""
    coordinator: EverUPSCoordinator = entry.runtime_data

    entities = [
        EverUPSNumber(coordinator, description)
        for description in NUMBER_DESCRIPTIONS
    ]

    async_add_entities(entities)


class EverUPSNumber(CoordinatorEntity[EverUPSCoordinator], NumberEntity):
    """Representation of an Ever UPS number."""

    entity_description: EverUPSNumberEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EverUPSCoordinator,
        description: EverUPSNumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number or coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info
        self._cached_value: float | None = None

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        return self._cached_value

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to Home Assistant."""
        await super().async_added_to_hass()
        # Read the initial value from registers
        await self._async_read_value()

    async def _async_read_value(self) -> None:
        """Read the current value from the UPS."""
        registers = await self.coordinator.async_read_registers(
            self.entity_description.register_address, 2
        )
        if registers is not None:
            # Combine MSB and LSB into a 32-bit value
            # Registers are: [MSB_high, MSB_low] stored as two 16-bit words
            self._cached_value = float((registers[0] << 16) | registers[1])
            self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        int_value = int(value)
        
        # Split into two 16-bit registers (MSB and LSB)
        msb = (int_value >> 16) & 0xFFFF
        lsb = int_value & 0xFFFF
        
        _LOGGER.debug(
            "Setting %s to %d (MSB: %d, LSB: %d)",
            self.entity_description.key,
            int_value,
            msb,
            lsb,
        )
        
        success = await self.coordinator.async_write_registers(
            self.entity_description.register_address, [msb, lsb]
        )
        
        if success:
            self._cached_value = value
            self.async_write_ha_state()
            _LOGGER.info(
                "Successfully set %s to %d seconds",
                self.entity_description.key,
                int_value,
            )
        else:
            _LOGGER.error(
                "Failed to set %s to %d",
                self.entity_description.key,
                int_value,
            )
