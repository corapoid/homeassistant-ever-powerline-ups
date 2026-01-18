"""Sensor platform for Ever Powerline UPS."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfApparentPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EverUPSCoordinator


@dataclass(frozen=True, kw_only=True)
class EverUPSSensorEntityDescription(SensorEntityDescription):
    """Describes Ever UPS sensor entity."""

    value_key: str


SENSOR_DESCRIPTIONS: tuple[EverUPSSensorEntityDescription, ...] = (
    # Temperature
    EverUPSSensorEntityDescription(
        key="temperature",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="temperature",
    ),
    # Input
    EverUPSSensorEntityDescription(
        key="input_frequency",
        translation_key="input_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_frequency",
    ),
    EverUPSSensorEntityDescription(
        key="input_voltage_l1",
        translation_key="input_voltage_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_voltage_l1",
    ),
    EverUPSSensorEntityDescription(
        key="input_voltage_l2",
        translation_key="input_voltage_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_voltage_l2",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="input_voltage_l3",
        translation_key="input_voltage_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="input_voltage_l3",
        entity_registry_enabled_default=False,
    ),
    # Output voltage
    EverUPSSensorEntityDescription(
        key="output_voltage_l1",
        translation_key="output_voltage_l1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_voltage_l1",
    ),
    EverUPSSensorEntityDescription(
        key="output_voltage_l2",
        translation_key="output_voltage_l2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_voltage_l2",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="output_voltage_l3",
        translation_key="output_voltage_l3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_voltage_l3",
        entity_registry_enabled_default=False,
    ),
    # Output current
    EverUPSSensorEntityDescription(
        key="output_current_l1",
        translation_key="output_current_l1",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_current_l1",
    ),
    EverUPSSensorEntityDescription(
        key="output_current_l2",
        translation_key="output_current_l2",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_current_l2",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="output_current_l3",
        translation_key="output_current_l3",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="output_current_l3",
        entity_registry_enabled_default=False,
    ),
    # Active power
    EverUPSSensorEntityDescription(
        key="active_power_l1",
        translation_key="active_power_l1",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="active_power_l1",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="active_power_l2",
        translation_key="active_power_l2",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="active_power_l2",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="active_power_l3",
        translation_key="active_power_l3",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="active_power_l3",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="active_power_total",
        translation_key="active_power_total",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="active_power_total",
    ),
    # Apparent power
    EverUPSSensorEntityDescription(
        key="apparent_power_l1",
        translation_key="apparent_power_l1",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="apparent_power_l1",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="apparent_power_l2",
        translation_key="apparent_power_l2",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="apparent_power_l2",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="apparent_power_l3",
        translation_key="apparent_power_l3",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="apparent_power_l3",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="apparent_power_total",
        translation_key="apparent_power_total",
        native_unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
        device_class=SensorDeviceClass.APPARENT_POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="apparent_power_total",
    ),
    # Load
    EverUPSSensorEntityDescription(
        key="load_l1",
        translation_key="load_l1",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="load_l1",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="load_l2",
        translation_key="load_l2",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="load_l2",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="load_l3",
        translation_key="load_l3",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="load_l3",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="load_total",
        translation_key="load_total",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="load_total",
        icon="mdi:gauge",
    ),
    # Battery
    EverUPSSensorEntityDescription(
        key="battery_charge",
        translation_key="battery_charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_charge",
    ),
    EverUPSSensorEntityDescription(
        key="battery_voltage",
        translation_key="battery_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_voltage",
    ),
    EverUPSSensorEntityDescription(
        key="battery_voltage_pos",
        translation_key="battery_voltage_pos",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_voltage_pos",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="battery_voltage_neg",
        translation_key="battery_voltage_neg",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="battery_voltage_neg",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="runtime_remaining",
        translation_key="runtime_remaining",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="runtime_remaining",
        icon="mdi:timer-outline",
    ),
    # Bypass
    EverUPSSensorEntityDescription(
        key="bypass_frequency",
        translation_key="bypass_frequency",
        native_unit_of_measurement=UnitOfFrequency.HERTZ,
        device_class=SensorDeviceClass.FREQUENCY,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="bypass_frequency",
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="bypass_voltage",
        translation_key="bypass_voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_key="bypass_voltage",
        entity_registry_enabled_default=False,
    ),
    # Status sensors (enum-like)
    EverUPSSensorEntityDescription(
        key="operating_mode",
        translation_key="operating_mode",
        device_class=SensorDeviceClass.ENUM,
        value_key="operating_mode_name",
        icon="mdi:state-machine",
        options=[
            "Initialization",
            "Standby",
            "Bypass",
            "Online",
            "On Battery",
            "Battery Test",
            "Converter",
            "ECO",
            "Shutdown",
            "Boost",
            "Buck",
            "Other",
        ],
    ),
    EverUPSSensorEntityDescription(
        key="battery_status",
        translation_key="battery_status",
        device_class=SensorDeviceClass.ENUM,
        value_key="battery_status_name",
        icon="mdi:battery-heart-variant",
        options=["Normal", "Low", "Depleted", "Discharging", "Fault"],
    ),
    EverUPSSensorEntityDescription(
        key="battery_test_result",
        translation_key="battery_test_result",
        device_class=SensorDeviceClass.ENUM,
        value_key="test_result_name",
        icon="mdi:clipboard-check-outline",
        options=["No Test Performed", "In Progress", "Passed", "Failed", "Cancelled"],
        entity_registry_enabled_default=False,
    ),
    EverUPSSensorEntityDescription(
        key="abm_status",
        translation_key="abm_status",
        device_class=SensorDeviceClass.ENUM,
        value_key="abm_status_name",
        icon="mdi:battery-charging",
        options=["Charging", "Float Charging", "Resting", "Discharging", "Disabled"],
        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ever UPS sensors based on a config entry."""
    coordinator: EverUPSCoordinator = entry.runtime_data

    entities = [
        EverUPSSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    ]

    async_add_entities(entities)


class EverUPSSensor(CoordinatorEntity[EverUPSCoordinator], SensorEntity):
    """Representation of an Ever UPS sensor."""

    entity_description: EverUPSSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EverUPSCoordinator,
        description: EverUPSSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number or coordinator.host}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.value_key)
