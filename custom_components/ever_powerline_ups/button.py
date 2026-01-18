"""Button platform for Ever Powerline UPS."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    BATTERY_TEST_CANCEL,
    BATTERY_TEST_START,
    DOMAIN,
    REG_BATTERY_TEST,
)
from .coordinator import EverUPSCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EverUPSButtonEntityDescription(ButtonEntityDescription):
    """Describes Ever UPS button entity."""

    register_value: int


BUTTON_DESCRIPTIONS: tuple[EverUPSButtonEntityDescription, ...] = (
    EverUPSButtonEntityDescription(
        key="battery_test_start",
        translation_key="battery_test_start",
        icon="mdi:battery-sync",
        register_value=BATTERY_TEST_START,
    ),
    EverUPSButtonEntityDescription(
        key="battery_test_cancel",
        translation_key="battery_test_cancel",
        icon="mdi:battery-remove",
        register_value=BATTERY_TEST_CANCEL,
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ever UPS buttons based on a config entry."""
    coordinator: EverUPSCoordinator = entry.runtime_data

    entities = [
        EverUPSButton(coordinator, description)
        for description in BUTTON_DESCRIPTIONS
    ]

    async_add_entities(entities)


class EverUPSButton(CoordinatorEntity[EverUPSCoordinator], ButtonEntity):
    """Representation of an Ever UPS button."""

    entity_description: EverUPSButtonEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EverUPSCoordinator,
        description: EverUPSButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number or coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.debug(
            "Pressing button %s with value %d",
            self.entity_description.key,
            self.entity_description.register_value,
        )
        
        success = await self.coordinator.async_write_register(
            REG_BATTERY_TEST, self.entity_description.register_value
        )
        
        if success:
            _LOGGER.info(
                "Successfully sent command %s to UPS",
                self.entity_description.key,
            )
            # Refresh data after command
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error(
                "Failed to send command %s to UPS",
                self.entity_description.key,
            )
