"""Constants for the Ever Powerline UPS integration."""
from enum import IntEnum
from typing import Final

DOMAIN: Final = "ever_powerline_ups"

# Default configuration
DEFAULT_PORT: Final = 502
DEFAULT_SLAVE_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 10  # seconds

# Modbus register base addresses
REG_IDENTIFIERS: Final = 0x0000  # Length: 80 words
REG_WARNINGS: Final = 0x0060  # Length: 6 words
REG_STATUS: Final = 0x0070  # Length: 10 words
REG_MEASUREMENTS: Final = 0x0080  # Length: 80 words
REG_RATED: Final = 0x00E0  # Length: 16 words
REG_SETTINGS: Final = 0x00F0  # Length: 16 words
REG_TIMERS: Final = 0x0100  # Length: 4 words

# Identifier register offsets (from 0x0000)
REG_MANUFACTURER: Final = 0x0000  # 16 words (32 chars)
REG_MODEL: Final = 0x0010  # 32 words (64 chars)
REG_FIRMWARE: Final = 0x0030  # 8 words (16 chars)
REG_SERIAL: Final = 0x0038  # 8 words (16 chars)

# Warning register bit masks (address 0x0060)
WARNING_POWER_FAIL: Final = 0x8000  # Bit 15
WARNING_LOW_BATTERY: Final = 0x4000  # Bit 14
WARNING_UPS_FAILED: Final = 0x2000  # Bit 13
WARNING_ON_BATTERY: Final = 0x1000  # Bit 12
WARNING_TEST_IN_PROGRESS: Final = 0x0800  # Bit 11
WARNING_BYPASS_ON: Final = 0x0400  # Bit 10
WARNING_COMMUNICATION_LOST: Final = 0x0200  # Bit 9
WARNING_GOING_SHUTDOWN: Final = 0x0100  # Bit 8
WARNING_OVER_TEMPERATURE: Final = 0x0010  # Bit 4
WARNING_OVERLOAD: Final = 0x0008  # Bit 3

# Warning register bit masks (address 0x0061)
WARNING_EPO_ACTIVE: Final = 0x0400  # Bit 10
WARNING_MAIN_NEUTRAL_LOSS: Final = 0x0100  # Bit 8
WARNING_MAIN_PHASE_ERROR: Final = 0x0080  # Bit 7
WARNING_SITE_FAULT: Final = 0x0040  # Bit 6
WARNING_BYPASS_ABNORMAL: Final = 0x0020  # Bit 5
WARNING_BYPASS_PHASE_ERROR: Final = 0x0010  # Bit 4
WARNING_BATTERY_OPEN: Final = 0x0008  # Bit 3
WARNING_BATTERY_OVER_CHARGE: Final = 0x0004  # Bit 2

# Warning register bit masks (address 0x0062)
WARNING_OVERLOAD_WARNING: Final = 0x8000  # Bit 15
WARNING_FAN_LOCK: Final = 0x4000  # Bit 14
WARNING_MAINTENANCE_COVER_OPEN: Final = 0x2000  # Bit 13
WARNING_CHARGER_FAULT: Final = 0x1000  # Bit 12

# Measurement register addresses
REG_TEMPERATURE: Final = 0x0080  # 0.1 C
REG_INPUT_FREQUENCY: Final = 0x0081  # 0.1 Hz
REG_INPUT_VOLTAGE_L1: Final = 0x0084  # 0.1 V
REG_INPUT_VOLTAGE_L2: Final = 0x0085  # 0.1 V
REG_INPUT_VOLTAGE_L3: Final = 0x0086  # 0.1 V
REG_OUTPUT_VOLTAGE_L1: Final = 0x0093  # 0.1 V
REG_OUTPUT_VOLTAGE_L2: Final = 0x0094  # 0.1 V
REG_OUTPUT_VOLTAGE_L3: Final = 0x0095  # 0.1 V
REG_OUTPUT_CURRENT_L1: Final = 0x0099  # 0.1 A
REG_OUTPUT_CURRENT_L2: Final = 0x009A  # 0.1 A
REG_OUTPUT_CURRENT_L3: Final = 0x009B  # 0.1 A
REG_ACTIVE_POWER_L1: Final = 0x009C  # 100 W
REG_ACTIVE_POWER_L2: Final = 0x009D  # 100 W
REG_ACTIVE_POWER_L3: Final = 0x009E  # 100 W
REG_APPARENT_POWER_L1: Final = 0x009F  # 100 VA
REG_APPARENT_POWER_L2: Final = 0x00A0  # 100 VA
REG_APPARENT_POWER_L3: Final = 0x00A1  # 100 VA
REG_LOAD_L1: Final = 0x00A2  # %
REG_LOAD_L2: Final = 0x00A3  # %
REG_LOAD_L3: Final = 0x00A4  # %
REG_RUNTIME_MINUTES: Final = 0x00A5  # minutes
REG_RUNTIME_SECONDS: Final = 0x00A6  # seconds
REG_BATTERY_CHARGE: Final = 0x00A9  # %
REG_BATTERY_VOLTAGE_POS: Final = 0x00AA  # 0.1 V
REG_BATTERY_VOLTAGE_NEG: Final = 0x00AB  # 0.1 V
REG_BYPASS_FREQUENCY: Final = 0x00AD  # 0.1 Hz
REG_BYPASS_VOLTAGE: Final = 0x00B0  # 0.1 V

# Status register addresses
REG_UPS_TYPE: Final = 0x0070  # MSB: UPS type, LSB: Operating mode
REG_PHASE_COUNT: Final = 0x0071  # MSB: Input phases, LSB: Output phases
REG_BATTERY_STATUS: Final = 0x0072  # MSB: Battery status, LSB: Test result
REG_INPUT_SOURCE: Final = 0x0073  # MSB: Input source, LSB: Bypass phases
REG_ABM_STATUS: Final = 0x0074  # MSB: Cell position, LSB: ABM status

# Rated data register addresses
REG_RATED_APPARENT_POWER: Final = 0x00E1  # 100 VA
REG_RATED_BATTERY_VOLTAGE: Final = 0x00E2  # 0.1 V
REG_RATED_OUTPUT_VOLTAGE: Final = 0x00E4  # 0.1 V
REG_RATED_OUTPUT_FREQUENCY: Final = 0x00E5  # 0.1 Hz
REG_RATED_ACTIVE_POWER: Final = 0x00E6  # 100 W
REG_LOAD_SEGMENT_SUPPORT: Final = 0x00EB  # 1 = yes, 0 = no
REG_LOAD_SEGMENT_COUNT: Final = 0x00EC  # 0, 1, or 2

# Settings register addresses
REG_BATTERY_TEST: Final = 0x00F0  # 1 = start, 3 = cancel
REG_SHUTDOWN_DELAY_MSB: Final = 0x0100  # seconds (MSB)
REG_SHUTDOWN_DELAY_LSB: Final = 0x0101  # seconds (LSB)
REG_STARTUP_DELAY_MSB: Final = 0x0102  # seconds (MSB)
REG_STARTUP_DELAY_LSB: Final = 0x0103  # seconds (LSB)

# Battery test commands
BATTERY_TEST_START: Final = 1
BATTERY_TEST_CANCEL: Final = 3


class UPSType(IntEnum):
    """UPS type enumeration."""

    ONLINE = 0
    OFFLINE = 1


class OperatingMode(IntEnum):
    """UPS operating mode enumeration."""

    INITIALIZATION = 1
    STANDBY = 2
    BYPASS = 3
    ONLINE = 4
    BATTERY = 5
    BATTERY_TEST = 6
    CONVERTER = 8
    ECO = 9
    SHUTDOWN = 10
    BOOST = 11
    BUCK = 12
    OTHER = 13


OPERATING_MODE_NAMES: Final = {
    OperatingMode.INITIALIZATION: "Initialization",
    OperatingMode.STANDBY: "Standby",
    OperatingMode.BYPASS: "Bypass",
    OperatingMode.ONLINE: "Online",
    OperatingMode.BATTERY: "On Battery",
    OperatingMode.BATTERY_TEST: "Battery Test",
    OperatingMode.CONVERTER: "Converter",
    OperatingMode.ECO: "ECO",
    OperatingMode.SHUTDOWN: "Shutdown",
    OperatingMode.BOOST: "Boost",
    OperatingMode.BUCK: "Buck",
    OperatingMode.OTHER: "Other",
}


class BatteryStatus(IntEnum):
    """Battery status enumeration."""

    NORMAL = 2
    LOW = 3
    DEPLETED = 4
    DISCHARGING = 5
    FAULT = 6


BATTERY_STATUS_NAMES: Final = {
    BatteryStatus.NORMAL: "Normal",
    BatteryStatus.LOW: "Low",
    BatteryStatus.DEPLETED: "Depleted",
    BatteryStatus.DISCHARGING: "Discharging",
    BatteryStatus.FAULT: "Fault",
}


class BatteryTestResult(IntEnum):
    """Battery test result enumeration."""

    NO_TEST = 1
    IN_PROGRESS = 2
    PASSED = 3
    FAILED = 4
    CANCELLED = 6


BATTERY_TEST_RESULT_NAMES: Final = {
    BatteryTestResult.NO_TEST: "No Test Performed",
    BatteryTestResult.IN_PROGRESS: "In Progress",
    BatteryTestResult.PASSED: "Passed",
    BatteryTestResult.FAILED: "Failed",
    BatteryTestResult.CANCELLED: "Cancelled",
}


class ABMStatus(IntEnum):
    """ABM (Advanced Battery Management) status enumeration."""

    CHARGING = 1
    FLOAT_CHARGING = 2
    RESTING = 3
    DISCHARGING = 4
    DISABLED = 5


ABM_STATUS_NAMES: Final = {
    ABMStatus.CHARGING: "Charging",
    ABMStatus.FLOAT_CHARGING: "Float Charging",
    ABMStatus.RESTING: "Resting",
    ABMStatus.DISCHARGING: "Discharging",
    ABMStatus.DISABLED: "Disabled",
}

# Platforms
PLATFORMS: Final = ["sensor", "binary_sensor", "button", "number"]

# Config entry data keys
CONF_HOST: Final = "host"
CONF_PORT: Final = "port"

# Coordinator data keys
DATA_COORDINATOR: Final = "coordinator"
DATA_DEVICE_INFO: Final = "device_info"
