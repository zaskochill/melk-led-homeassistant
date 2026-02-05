# MELK LED Strip Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)

Home Assistant integration for MELK LED Strip controllers (JSK-P22 and similar) via Bluetooth.

## 🎉 What's New in v1.0.2

- 🐛 **Fixed:** Eliminated flickering/flashing of static color when turning on effects
- ✨ **Improved:** Smoother effect transitions
- 🔧 **Enhanced:** Better state restoration logic

See [CHANGELOG.md](CHANGELOG.md) for full details.

## Features

- ✅ RGB color control (16 million colors)
- ✅ Brightness adjustment
- ✅ **213 built-in effects** + **28 scenes** (241 total!)
- ✅ Microphone mode with music sync
- ✅ 8 EQ presets for microphone mode
- ✅ Adjustable sensitivity and effect speed
- ✅ State persistence after restart
- ✅ Automatic Bluetooth reconnection
- ✅ **Effect memory** (restores last effect on power on)
- ✅ **No flickering** when switching effects

## Supported Devices

- MELK LED Strip (JSK-P22)
- ELK-BLEDOM compatible controllers
- Similar Bluetooth LED strip controllers

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots (⋮) in the top right corner
4. Select "Custom repositories"
5. Add repository URL: `https://github.com/zaskochill/melk-led-homeassistant`
6. Select category: "Integration"
7. Click "Add"
8. Find "MELK LED Strip" in the list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/melk_led` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"MELK LED Strip"**
4. Select your device from the discovered list
5. Click **"Submit"**

Your device will be added with the following entities:
- **Light** - Main control (color, brightness, effects)
- **Switch** - Microphone mode
- **Select** - Microphone EQ mode
- **Number** - Microphone sensitivity
- **Number** - Effect speed

## Usage

### Basic Control
- Turn on/off the light
- Change color using the color picker
- Adjust brightness

### Effects
Select from **241 effects** including:
- **213 RGB effects:** Water, Rainbow, Breathing, Transition, Running, Curtain, Flow, Tail, and more!
- **28 special scenes:** Sunrise, Sunset, Birthday, Candlelight, Fireworks, Party, Christmas, and more!

The integration remembers your last effect and restores it when you turn the light back on.

### Microphone Mode (Music Sync)
1. Enable the "Microphone Mode" switch
2. Choose EQ preset (Energic, Rhythm, Spectrum, Rolling, etc.)
3. Adjust sensitivity if needed
4. Your LED strip will react to music and sounds!

## Troubleshooting

### Device not discovered
- Make sure the LED strip is powered on
- Check that Bluetooth is enabled on your Home Assistant device
- Try restarting the LED strip

### State not restored after restart
- This is normal for Bluetooth devices (they can't send state back)
- The integration saves the last state and restores it automatically
- If state is incorrect, simply turn off and on the light

## Technical Details

- **Protocol:** Bluetooth Low Energy (BLE)
- **Communication:** One-way commands (no feedback from device)
- **State Management:** Local storage with automatic restore

## Credits

Based on the ELK-BLEDOM protocol analysis and reverse engineering.

## License

MIT License

## Support

If you encounter any issues:
1. Check the [Issues](https://github.com/zaskochill/melk-led-homeassistant/issues) page
2. Enable debug logging in Home Assistant
3. Create a new issue with logs attached
