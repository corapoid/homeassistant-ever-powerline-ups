# Ever Powerline UPS Integration for Home Assistant

<p align="center">
  <img src="https://raw.githubusercontent.com/corapoid/homeassistant-ever-powerline-ups/main/image.png" alt="Ever Power Systems Logo" width="300">
</p>

<p align="center">
  <a href="https://github.com/hacs/integration"><img src="https://img.shields.io/badge/HACS-Custom-41BDF5.svg" alt="HACS"></a>
  <a href="https://github.com/corapoid/homeassistant-ever-powerline-ups/releases"><img src="https://img.shields.io/github/release/corapoid/homeassistant-ever-powerline-ups.svg" alt="GitHub Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/corapoid/homeassistant-ever-powerline-ups.svg" alt="License"></a>
</p>

Home Assistant integration for **Ever Powerline RT Pro** and **Powerline Multi** UPS devices via Modbus TCP.

## Supported Devices

- Ever Powerline RT Pro 1k-3k
- Ever Powerline Multi 10k / 20k

## Features

### Sensors
- **Temperature** - Internal UPS temperature
- **Input voltage/frequency** - Mains power measurements (L1, L2, L3)
- **Output voltage/current** - UPS output measurements (L1, L2, L3)
- **Active/Apparent power** - Power consumption (per phase and total)
- **Load** - Output load percentage
- **Battery charge** - Battery state of charge
- **Battery voltage** - Battery bank voltage
- **Runtime remaining** - Estimated backup time
- **Operating mode** - Current UPS mode (Online, Battery, Bypass, ECO, etc.)
- **Battery status** - Battery health status
- **ABM status** - Advanced Battery Management status

### Binary Sensors (Alarms)
- Power fail / On battery
- Low battery
- UPS failed
- Bypass active
- Over temperature
- Overload
- Fan fault
- Charger fault
- Battery open
- And more...

### Controls
- **Battery test** - Start/cancel battery self-test
- **Shutdown delay** - Scheduled shutdown time (seconds)
- **Startup delay** - Scheduled startup time (seconds)

## Requirements

- Ever Powerline UPS with Modbus TCP support (network card)
- Home Assistant 2024.1.0 or newer
- Network connectivity to UPS

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/corapoid/homeassistant-ever-powerline-ups` as repository
6. Select "Integration" as category
7. Click "Add"
8. Search for "Ever Powerline UPS" and install it
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from GitHub
2. Copy the `custom_components/ever_powerline_ups` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Search for "Ever Powerline UPS"
4. Enter the IP address and port (default: 502) of your UPS
5. Click **Submit**

The integration will automatically detect your UPS model and serial number.

## Modbus Connection

The integration uses **Modbus TCP** protocol to communicate with the UPS. Ensure that:

- Your UPS has a network card installed (SNMP/Modbus card)
- The UPS is connected to your network
- Port 502 (default Modbus port) is accessible
- Modbus TCP is enabled in the UPS network card settings

### Default Settings

| Parameter | Value |
|-----------|-------|
| Port | 502 |
| Slave ID | 1 |
| Scan interval | 10 seconds |

## Entity Naming

Entities are created with the following naming convention:
- `sensor.ever_<model>_<measurement>`
- `binary_sensor.ever_<model>_<alarm>`
- `button.ever_<model>_<action>`
- `number.ever_<model>_<setting>`

## Troubleshooting

### Cannot connect to UPS

1. Verify the UPS IP address is correct
2. Check if port 502 is open: `telnet <ups_ip> 502`
3. Ensure Modbus TCP is enabled on the UPS network card
4. Check firewall settings

### Sensors show unavailable

1. Check the UPS connection status
2. Review Home Assistant logs for Modbus errors
3. Try restarting the integration

### Debug Logging

Add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.ever_powerline_ups: debug
    pymodbus: debug
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not affiliated with or endorsed by Ever Sp. z o.o. Use at your own risk.

## Support

If you encounter any issues, please [open an issue](https://github.com/corapoid/homeassistant-ever-powerline-ups/issues) on GitHub.
