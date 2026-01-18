"""Binary sensor platform for Ever Powerline UPS."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    WARNING_BATTERY_OPEN,
    WARNING_BATTERY_OVER_CHARGE,
    WARNING_BYPASS_ABNORMAL,
    WARNING_BYPASS_ON,
    WARNING_BYPASS_PHASE_ERROR,
    WARNING_CHARGER_FAULT,
    WARNING_COMMUNICATION_LOST,
    WARNING_EPO_ACTIVE,
    WARNING_FAN_LOCK,
    WARNING_GOING_SHUTDOWN,
    WARNING_LOW_BATTERY,
    WARNING_MAIN_NEUTRAL_LOSS,
    WARNING_MAIN_PHASE_ERROR,
    WARNING_MAINTENANCE_COVER_OPEN,
    WARNING_ON_BATTERY,
    WARNING_OVER_TEMPERATURE,
    WARNING_OVERLOAD,
    WARNING_OVERLOAD_WARNING,
    WARNING_POWER_FAIL,
    WARNING_SITE_FAULT,
    WARNING_TEST_IN_PROGRESS,
    WARNING_UPS_FAILED,
)
from .coordinator import EverUPSCoordinator


@dataclass(frozen=True, kw_only=True)
class EverUPSBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Ever UPS binary sensor entity."""

    warning_register: str  # "warnings_0", "warnings_1", or "warnings_2"
    warning_mask: int


BINARY_SENSOR_DESCRIPTIONS: tuple[EverUPSBinarySensorEntityDescription, ...] = (
    # Register 0x0060
    EverUPSBinarySensorEntityDescription(
        key="power_fail",
        translation_key="power_fail",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_0",
        warning_mask=WARNING_POWER_FAIL,
        icon="mdi:power-plug-off",
    ),
    EverUPSBinarySensorEntityDescription(
        key="low_battery",
        translation_key="low_battery",
        device_class=BinarySensorDeviceClass.BATTERY,
        warning_register="warnings_0",
        warning_mask=WARNING_LOW_BATTERY,
    ),
    EverUPSBinarySensorEntityDescription(
        key="ups_failed",
        translation_key="ups_failed",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_0",
        warning_mask=WARNING_UPS_FAILED,
        icon="mdi:alert-circle",
    ),
    EverUPSBinarySensorEntityDescription(
        key="on_battery",
        translation_key="on_battery",
        device_class=BinarySensorDeviceClass.RUNNING,
        warning_register="warnings_0",
        warning_mask=WARNING_ON_BATTERY,
        icon="mdi:battery-arrow-down",
    ),
    EverUPSBinarySensorEntityDescription(
        key="test_in_progress",
        translation_key="test_in_progress",
        device_class=BinarySensorDeviceClass.RUNNING,
        warning_register="warnings_0",
        warning_mask=WARNING_TEST_IN_PROGRESS,
        icon="mdi:test-tube",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="bypass_active",
        translation_key="bypass_active",
        device_class=BinarySensorDeviceClass.RUNNING,
        warning_register="warnings_0",
        warning_mask=WARNING_BYPASS_ON,
        icon="mdi:swap-horizontal",
    ),
    EverUPSBinarySensorEntityDescription(
        key="communication_lost",
        translation_key="communication_lost",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        warning_register="warnings_0",
        warning_mask=WARNING_COMMUNICATION_LOST,
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="going_shutdown",
        translation_key="going_shutdown",
        device_class=BinarySensorDeviceClass.RUNNING,
        warning_register="warnings_0",
        warning_mask=WARNING_GOING_SHUTDOWN,
        icon="mdi:power-standby",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="over_temperature",
        translation_key="over_temperature",
        device_class=BinarySensorDeviceClass.HEAT,
        warning_register="warnings_0",
        warning_mask=WARNING_OVER_TEMPERATURE,
    ),
    EverUPSBinarySensorEntityDescription(
        key="overload",
        translation_key="overload",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_0",
        warning_mask=WARNING_OVERLOAD,
        icon="mdi:flash-alert",
    ),
    # Register 0x0061
    EverUPSBinarySensorEntityDescription(
        key="epo_active",
        translation_key="epo_active",
        device_class=BinarySensorDeviceClass.SAFETY,
        warning_register="warnings_1",
        warning_mask=WARNING_EPO_ACTIVE,
        icon="mdi:stop-circle",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="main_neutral_loss",
        translation_key="main_neutral_loss",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_MAIN_NEUTRAL_LOSS,
        icon="mdi:flash-off",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="main_phase_error",
        translation_key="main_phase_error",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_MAIN_PHASE_ERROR,
        icon="mdi:flash-off",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="site_fault",
        translation_key="site_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_SITE_FAULT,
        icon="mdi:swap-horizontal-variant",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="bypass_abnormal",
        translation_key="bypass_abnormal",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_BYPASS_ABNORMAL,
        icon="mdi:swap-horizontal",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="bypass_phase_error",
        translation_key="bypass_phase_error",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_BYPASS_PHASE_ERROR,
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="battery_open",
        translation_key="battery_open",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_BATTERY_OPEN,
        icon="mdi:battery-off",
    ),
    EverUPSBinarySensorEntityDescription(
        key="battery_over_charge",
        translation_key="battery_over_charge",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_1",
        warning_mask=WARNING_BATTERY_OVER_CHARGE,
        icon="mdi:battery-alert",
        entity_registry_enabled_default=False,
    ),
    # Register 0x0062
    EverUPSBinarySensorEntityDescription(
        key="overload_warning",
        translation_key="overload_warning",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_2",
        warning_mask=WARNING_OVERLOAD_WARNING,
        icon="mdi:flash-alert-outline",
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="fan_fault",
        translation_key="fan_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_2",
        warning_mask=WARNING_FAN_LOCK,
        icon="mdi:fan-alert",
    ),
    EverUPSBinarySensorEntityDescription(
        key="maintenance_cover_open",
        translation_key="maintenance_cover_open",
        device_class=BinarySensorDeviceClass.DOOR,
        warning_register="warnings_2",
        warning_mask=WARNING_MAINTENANCE_COVER_OPEN,
        entity_registry_enabled_default=False,
    ),
    EverUPSBinarySensorEntityDescription(
        key="charger_fault",
        translation_key="charger_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        warning_register="warnings_2",
        warning_mask=WARNING_CHARGER_FAULT,
        icon="mdi:battery-charging-wireless-alert",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ever UPS binary sensors based on a config entry."""
    coordinator: EverUPSCoordinator = entry.runtime_data

    entities = [
        EverUPSBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    ]

    async_add_entities(entities)


class EverUPSBinarySensor(CoordinatorEntity[EverUPSCoordinator], BinarySensorEntity):
    """Representation of an Ever UPS binary sensor."""

    entity_description: EverUPSBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EverUPSCoordinator,
        description: EverUPSBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number or coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.coordinator.data is None:
            return None
        
        register_value = self.coordinator.data.get(
            self.entity_description.warning_register, 0
        )
        return bool(register_value & self.entity_description.warning_mask)
