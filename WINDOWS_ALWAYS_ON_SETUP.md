# Setting Up Grok-VIS as an Always-On AI Assistant on Windows

This guide explains how to set up Grok-VIS to run continuously as a background service on Windows.

## Option 1: Using Windows Task Scheduler

### Quick Start

1. **Create a Windows Scheduled Task**:
   ```
   create_windows_task.bat
   ```
   This will create a task that starts Grok-VIS automatically when you log in.

2. **Manage Grok-VIS**:
   ```
   manage_grokvis.bat
   ```
   Use this script to start, stop, check status, and view logs.

### Manual Control with Task Scheduler

- Start: `schtasks /run /tn "GrokVIS_AI_Assistant"`
- Query status: `schtasks /query /tn "GrokVIS_AI_Assistant"`
- Delete task: `schtasks /delete /tn "GrokVIS_AI_Assistant" /f`

## Option 2: Using NSSM (More Robust)

For a more robust solution that runs as a true Windows service (starts before login, runs in background):

1. **Download NSSM**:
   - Get it from https://nssm.cc/download
   - Extract and add to your PATH (or copy nssm.exe to the Grok-VIS directory)

2. **Install as a Service**:
   ```
   nssm_install_service.bat
   ```
   This will install Grok-VIS as a Windows service that starts automatically with your computer.

3. **Control the Service**:
   ```
   net start GrokVIS
   net stop GrokVIS
   ```

## Accessing the Web Dashboard

Once Grok-VIS is running, you can access the web dashboard at:
```
http://localhost:5000
```

## Troubleshooting

If Grok-VIS isn't starting properly:

1. Check if Python is in your PATH environment variable
2. Verify that all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```
3. Check the logs in the `logs` directory
4. For Task Scheduler issues, check the Windows Event Viewer
5. For NSSM service issues, check the service logs:
   ```
   logs\grokvis.out.log
   logs\grokvis.err.log
   ```

## Comparing the Two Methods

- **Task Scheduler**: Simpler, but only runs when you're logged in
- **NSSM Service**: More robust, runs even when no user is logged in, automatically restarts if it crashes