# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-01-18

### Fixed
- Added debug logging for connection troubleshooting
- Added pymodbus version logging for compatibility checking
- Improved error diagnostics during config flow

### Added
- Verbose logging output for connection tests
- Pymodbus version info in logs

## [1.0.2] - 2026-01-18

### Fixed
- Pymodbus v3.x API compatibility (corrected)
- Slave ID only passed to read/write methods, not client initialization
- Removed `slave` parameter from AsyncModbusTcpClient constructor
- Slave ID correctly passed to read/write method calls:
  - `read_holding_registers()`
  - `write_register()`
  - `write_registers()`
  - `read_registers()`

This fixes `TypeError: AsyncModbusTcpClient.__init__() got an unexpected keyword argument 'slave'` when adding Ever Powerline UPS integration.

## [1.0.1] - 2026-01-18

### Fixed
- Pymodbus v3.x API compatibility
- Moved slave ID to client initialization
- Removed deprecated `slave` parameter from read/write methods
- Fixes connection error when adding Ever Powerline UPS integration

## [1.0.0] - 2026-01-18

### Added
- Initial release
- Support for Ever Powerline RT Pro 1k-3k and Powerline Multi 10k/20k
- Modbus TCP communication
- **Sensors:**
  - Temperature (internal UPS temperature)
  - Input frequency and voltage (L1, L2, L3)
  - Output voltage and current (L1, L2, L3)
  - Active power (per phase and total)
  - Apparent power (per phase and total)
  - Load percentage (per phase and total)
  - Battery charge level
  - Battery voltage (total, positive, negative)
  - Runtime remaining
  - Bypass frequency and voltage
  - Operating mode (Online, Battery, Bypass, ECO, etc.)
  - Battery status
  - Battery test result
  - ABM (Advanced Battery Management) status
- **Binary Sensors (Alarms):**
  - Power fail
  - Low battery
  - UPS failed
  - On battery
  - Test in progress
  - Bypass active
  - Communication lost
  - Going shutdown
  - Over temperature
  - Overload / Overload warning
  - EPO active
  - Main neutral loss
  - Main phase error
  - Site fault (L/N swapped)
  - Bypass abnormal
  - Bypass phase error
  - Battery open
  - Battery over charge
  - Fan fault
  - Maintenance cover open
  - Charger fault
- **Buttons:**
  - Start battery test
  - Cancel battery test
- **Number entities:**
  - Shutdown delay (seconds)
  - Startup delay (seconds)
- Config flow for easy setup via UI
- Translations: English, Polish
- HACS compatibility

### Technical Details
- Uses pymodbus library for Modbus TCP communication
- 10-second polling interval
- Slave ID: 1 (fixed)
- Default port: 502
