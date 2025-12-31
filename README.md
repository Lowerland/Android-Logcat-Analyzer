# Android Logcat Analyzer

This tool helps you capture and analyze Android logcat output, which can be overwhelming with lots of activity.

## Prerequisites

- ADB (Android Debug Bridge) installed and in PATH
- Android device connected via USB with USB debugging enabled
- Python 3.x installed

## Quick Start

### 1. Check if your device is connected:
```bash
adb devices
```

### 2. Run the analyzer:
```bash
python logcat_analyzer.py
```

## Features

- **Capture logcat**: Record logcat for a specified duration (10 or 30 seconds)
- **Analyze statistics**: View log level distribution, most active tags, and top errors/warnings
- **Filter by level**: Extract only errors (E) or warnings (W)
- **Filter by tag**: Extract logs from specific app/component tags
- **Search keywords**: Find specific text in logs
- **Live stream**: View logcat in real-time

## Common Use Cases

### Find errors only:
```bash
adb logcat -v time *:E
```

### Filter by app package:
```bash
adb logcat -v time | findstr "com.your.app"
```

### Clear and monitor fresh logs:
```bash
adb logcat -c
adb logcat -v time
```

### Save to file:
```bash
adb logcat -v time > logcat_output.txt
```

## Understanding Log Levels

- **V (Verbose)**: Most detailed, usually not needed
- **D (Debug)**: Debug messages for development
- **I (Info)**: General information messages
- **W (Warning)**: Potential issues that aren't errors
- **E (Error)**: Actual errors that should be investigated
- **F (Fatal)**: Critical errors causing crashes

## Tips for Managing Heavy Logcat Output

1. **Use filters**: Focus on specific log levels or tags
2. **Clear old logs**: Use `adb logcat -c` before capturing
3. **Use time format**: `-v time` shows timestamps
4. **Filter by priority**: `*:W` shows only warnings and above
5. **Grep/findstr**: Pipe output to search for specific terms
