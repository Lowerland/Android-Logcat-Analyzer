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


### Example:

```bash
PS E:\vscode\adb> python logcat_analyzer.py
Android Logcat Analyzer
============================================================

Options:
1. Capture new logcat (10 seconds)
2. Capture new logcat (30 seconds)
3. Analyze existing logcat.txt
4. Filter by error level (E)
5. Filter by warning level (W)
6. Filter by tag
7. Search for keyword
8. Get live logcat stream (Ctrl+C to stop)
9. 📋 Generate critical issues report
10. 🔍 Monitor specific app/component

Enter your choice (1-10): 1

Capturing logcat for 10 seconds...
Logcat captured and saved to logcat.txt

============================================================
LOGCAT ANALYSIS: logcat.txt
============================================================

📊 LOG LEVEL DISTRIBUTION:
  E (Error   ):    147 ( 5.37%)
  W (Warning ):    116 ( 4.24%)
  I (Info    ):   1557 (56.87%)
  D (Debug   ):    883 (32.25%)
  V (Verbose ):     35 ( 1.28%)

📝 TOTAL LOG ENTRIES: 2738

🏷️  TOP 10 MOST ACTIVE TAGS:
     740 - ULELite
     160 - SDP.SysUi.BaseSeedling
     135 - IWlanJni
      96 - [UAH_CLIENT]
      93 - QmiClient
      66 - SatelliteController
      60 - UTrace.Sdk.App
      40 - SDP.SysUi.EngineViewProxy
      40 - msys
      37 - vendor.qti.bluetooth@1.1-ibs_handler

❌ ERRORS FOUND (147 total):
  1. ANDR-PERF-RESOURCEQS: ANDR-PERF-RESOURCEQS: AddAndApply() 125: Resource with major=16, minor=0 not supported
  2. APS_ALOG: CAM_ALOG_LIMIT,Fatal Err! mFd -1
  3. APS_ALOG: CAM_ALOG_LIMIT,Fatal Err! FilePath nullptr!
  4. APS_ALOG: Failed to open directory
  5. APS_ALOG: FileALogWriter: file open failed /data/vendor/cam_alog_-_10-1_199925_7904_01.txt
  6. APS_ALOG: Unable to open file. Please disable SELinux and restart camerahalserver. !!!
  7. ANDR-PERF-RESOURCEQS: ANDR-PERF-RESOURCEQS: AddAndApply() 125: Resource with major=16, minor=0 not supported
  8. vendor.qti.bluetooth@1.1-wake_lock: Release wake lock not initialized/acquired
  9. ANDR-PERF-RESOURCEQS: ANDR-PERF-RESOURCEQS: AddAndApply() 125: Resource with major=16, minor=0 not supported
  10. OplusStorageUFSBandwidth: storage_io_metrics_path is /proc/oplus_storage/io_metrics/forever/
  ... and 137 more errors

⚠️  WARNINGS FOUND (116 total):
  1. RTCDGWService.cpp: DGW: StreamGroup reconnection throttled; reconnecting in 776
  2. OPLUS_LOG_LOAD: ==LOGS PROG INFO, prog(com.android.systemui) ==
  3. PantaCard.SysUi.SeedlingCard: 9999006&27&20_sid=989090006_rk=8399c5,checkShouldStopRefreshingCard return false,because shouldInt
  4. ULELite: [JsCardParser.StatusBar37notification_sm] UNEXPECTED: no eventHandler key  eventType ==>changeeventH
  5. ULELite: [JsCardParser.StatusBar38notification_lg] UNEXPECTED: no eventHandler key  eventType ==>changeeventH
  6. OPLUS_LOG_LOAD: ==LOGS PROG INFO, prog(com.oplus.camera) ==
  7. OPLUS_LOG_LOAD: ==LOGS PROG INFO, prog(system_server) ==
  8. LibevQuicAsyncUDPSocket.h: setTosOrTrafficClass not implemented in LibevQuicAsyncUDPSocket
  9. RTCDGWService.cpp: DGW: StreamGroup reconnection throttled; reconnecting in 778
  10. PantaCard.SysUi.SeedlingCard: 9999006&27&20_sid=989090006_rk=899c5,checkShouldStopRefreshingCard return false,because shouldInt
  ... and 106 more warnings

============================================================
```


### Generate critical issues report

```bash
PS E:\vscode\adb> python logcat_analyzer.py
Android Logcat Analyzer
============================================================

Options:
1. Capture new logcat (10 seconds)
2. Capture new logcat (30 seconds)
3. Analyze existing logcat.txt
4. Filter by error level (E)
5. Filter by warning level (W)
6. Filter by tag
7. Search for keyword
8. Get live logcat stream (Ctrl+C to stop)
9. 📋 Generate critical issues report
10. 🔍 Monitor specific app/component

Enter your choice (1-10): 9

📋 Generating critical issues report...

✅ Critical issues report saved to: critical_report.txt
   Total Errors: 147
   Total Warnings: 116
   Unique Error Types: 30

💡 Tip: Open 'critical_report.txt' to view the detailed analysis
PS E:\vscode\adb> 
```

### critical issues report

```bash
================================================================================
ANDROID LOGCAT - CRITICAL ISSUES REPORT
================================================================================

Analysis Date: 2025-12-31 14:45:17
Source File: logcat.txt
Total Errors: 147
Total Warnings: 116

================================================================================

🚨 PRIORITY 1: MOST FREQUENT ERRORS
--------------------------------------------------------------------------------
  [32x] ANDR-PERF-RESOURCEQS: ANDR-PERF-RESOURCEQS: AddAndApply() 125: Resource 
  [20x] msys: E[N mns]_OnDiskCacheGetData(632)=>Start post callb
  [20x] msys: E[N mns]_LogError(228)=>Failed to resolve using sy
  [11x] MvfstCallbacks.cpp: onConnectionSetupError: error=TransportError: Inte
  [9x] SatelliteController: registerForSatelliteModemStateChanged: mSatelliteS
  [5x] vendor.qti.bluetooth@1.1-wake_lock: Release wake lock not initialized/acquired
  [5x] OplusStorageUFSBandwidth: storage_io_metrics_path is /proc/oplus_storage/io_
  [5x] OplusStorageUFSBandwidth: Alarm set to trigger in 10 seconds
  [4x] OplusStorageUFSBandwidth: Bandwidth - Read: 0,00 MB/s, Write: 0,00 MB/s
  [4x] vendor.qti.bluetooth@1.1-wake_lock: Acquire write to wakelock file failed -1 - Operati

⚠️  PRIORITY 2: COMPONENTS WITH MOST ERRORS
--------------------------------------------------------------------------------
   40 errors - msys
   32 errors - ANDR-PERF-RESOURCEQS
   20 errors - OplusStorageUFSBandwidth
   11 errors - MvfstCallbacks.cpp
   10 errors - APS_ALOG
    9 errors - vendor.qti.bluetooth@1.1-wake_lock
    9 errors - SatelliteController
    6 errors - msgr.msys
    4 errors - Thing-Network
    3 errors - oplus_bt_power

📝 PRIORITY 3: UNIQUE ERROR MESSAGES (First 20)
--------------------------------------------------------------------------------

[12-31 14:40:25.305] ANDR-PERF-RESOURCEQS
  ANDR-PERF-RESOURCEQS: AddAndApply() 125: Resource with major=16, minor=0 not supported

[12-31 14:40:25.527] APS_ALOG
  CAM_ALOG_LIMIT,Fatal Err! mFd -1

[12-31 14:40:25.527] APS_ALOG
  CAM_ALOG_LIMIT,Fatal Err! FilePath nullptr!

[12-31 14:40:25.528] APS_ALOG
  Failed to open directory

[12-31 14:40:25.528] APS_ALOG
  FileALogWriter: file open failed /data/vendor/cam_alog_2025_---14005_7004_01.txt

[12-31 14:40:25.528] APS_ALOG
  Unable to open file. Please disable SELinux and restart camerahalserver. !!!

[12-31 14:40:25.815] vendor.qti.bluetooth@1.1-wake_lock
  Release wake lock not initialized/acquired

[12-31 14:40:25.996] OplusStorageUFSBandwidth
  storage_io_metrics_path is /proc/oplus_storage/io_metrics/forever/

[12-31 14:40:25.997] OplusStorageUFSBandwidth
  Bandwidth - Read: 0,00 MB/s, Write: 0,00 MB/s

[12-31 14:40:25.997] OplusStorageUFSBandwidth
  Task time: 1ms

[12-31 14:40:26.001] OplusStorageUFSBandwidth
  Alarm set to trigger in 10 seconds

[12-31 14:40:26.128] msys
  E[N mns]_OnDiskCacheGetData(632)=>Start post callback cache refresh DNS resolution

[12-31 14:40:26.139] MvfstCallbacks.cpp
  onConnectionSetupError: error=TransportError: Internal Error, Error on socket write Operation not permitted,

[12-31 14:40:26.139] msys
  E[N mns]_LogError(228)=>Failed to resolve using system DNS resolver, getaddrinfo(): No address associated with hostname

[12-31 14:40:26.156] oplus_bt_power
  [oplus_bt_power.cc:145]  dcsar not support or not on

[12-31 14:40:26.158] vendor.qti.bluetooth@1.1-wake_lock
  Acquire write to wakelock file failed -1 - Operation not permitted

[12-31 14:40:27.603] msgr.TigonNetworkSessionListenerManager
  handleDataTask failed for handleDataTaskType

[12-31 14:40:27.606] msgr.msys
  E[N data-request]_HandleDataResponse(1984)=>Data request error for task 000-000-499EF5-B996-2B7995B920 (response type 1): network disconnected

[12-31 14:40:27.611] msgr.msys
  E[S sync]_createResponseError(269)=>Network Response 8888-898908905--20 contains sync error Error Domain=NSURLErrorDomain Code=1 UserInfo=0xb40080 {MCFErrorDirectUnderlyingErrorKey=0xb-88908900 "Error Domain=NSURLErrorDomain Code=1 UserInfo=0xb400890890 {MCFErrorDirectLocalizedFailureReasonKey=TigonError(error=TransientError, errorDomain=TigonLigerErrorDomain, domainErrorCode=3, tigonErrorClassname=TigonNetworkSessionListenerManager, analyticsDetail="AsyncSocketException: connect timed out after 29991ms, type = Timed out")}", MCFErrorDirectLocalizedFailureReasonKey=network disconnected} - Underlying error Error Domain=NSURLErrorDomain Code=1 UserInfo=890890 {MCFErrorDirectLocalizedFailureReasonKey=TigonError(error=TransientError, errorDomain=TigonLigerErrorDomain, domainErrorCode=3, tigonErrorClassname=TigonNetworkSessionListenerManager, analyticsDetail="AsyncSocketException: connect timed out after 29991ms, type = Timed out")}: Error Domain=NSURLErrorDomain Code=1 UserInfo=890809 {MCFErrorDirectUnderlyingErrorKey=0xb40890890-0-89 "Error Domain=NSURLErrorDomain Code=1 UserInfo=0xb4890890 {MCFErrorDirectLocalizedFailureReasonKey=TigonError(error=TransientError, errorDomain=TigonLigerErrorDomain, domainErrorCode=3, tigonErrorClassname=TigonNetworkSessionListenerManager, analyticsDetail="AsyncSocketException: connect timed out after 29991ms, type = Timed out")}", MCFErrorDirectLocalizedFailureReasonKey=network disconnected}

[12-31 14:40:28.005] OplusStorageUFSBandwidth
  Task time: 3ms

⚡ WARNING SUMMARY
--------------------------------------------------------------------------------
   20 warnings - ULELite
   16 warnings - ContextImpl
   16 warnings - KeyguardSecurityViewFlipper
   13 warnings - IWlanNetworkService
   11 warnings - RTCDGWService.cpp
   11 warnings - LibevQuicAsyncUDPSocket.h
   10 warnings - PantaCard.SysUi.SeedlingCard
   10 warnings - Settings
    3 warnings - OPLUS_LOG_LOAD
    2 warnings - JobService

💡 RECOMMENDATIONS
--------------------------------------------------------------------------------
1. Focus on components with repeated errors
2. Check network connectivity (DNS resolution failures)
3. Verify app permissions for socket operations
4. Review system resource configurations

================================================================================


```