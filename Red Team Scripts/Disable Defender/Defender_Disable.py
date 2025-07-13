import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_powershell(cmd):
    full_cmd = ["powershell", "-Command", cmd]
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, shell=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def disable_defender_powershell():
    print("[*] Disabling Microsoft Defender via PowerShell policies...")
    cmds = [
        # Disable real-time monitoring
        "Set-MpPreference -DisableRealtimeMonitoring $true",
        # Disable behavior monitoring
        "Set-MpPreference -DisableBehaviorMonitoring $true",
        # Disable script scanning
        "Set-MpPreference -DisableScriptScanning $true",
        # Disable network protection
        "Set-MpPreference -EnableNetworkProtection Disabled",
        # Disable antivirus
        "Set-MpPreference -DisableAntiSpyware $true",
        # Disable cloud protection
        "Set-MpPreference -DisableBlockAtFirstSeen $true",
        # Disable automatic sample submission
        "Set-MpPreference -SubmitSamplesConsent 2"
    ]

    for cmd in cmds:
        code, out, err = run_powershell(cmd)
        if code == 0:
            print(f"  [+] Successfully ran: {cmd}")
        else:
            print(f"  [-] Failed to run: {cmd}\n    Error: {err.strip()}")

def disable_defender_registry():
    print("[*] Disabling Microsoft Defender via Registry edits...")
    reg_cmds = [
        # Disable AntiSpyware
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f',
        # Disable Real-time Protection
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f',
        # Disable Behavior Monitoring
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f',
        # Disable On Access Protection
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f',
        # Disable Scheduled Scans
        'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Scan" /v "DisableScheduledScan" /t REG_DWORD /d 1 /f',
    ]

    for cmd in reg_cmds:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  [+] Registry key set successfully: {cmd}")
            else:
                print(f"  [-] Failed to set registry key: {cmd}\n    Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"  [-] Exception running registry command: {cmd}\n    Exception: {e}")

def stop_defender_services():
    print("[*] Attempting to stop Microsoft Defender services...")
    services = [
        "WinDefend",  # Windows Defender Antivirus Service
        "WdNisSvc",   # Windows Defender Network Inspection Service
    ]

    for service in services:
        try:
            # Stop the service
            subprocess.run(f"sc stop {service}", shell=True, capture_output=True)
            # Disable the service
            subprocess.run(f"sc config {service} start= disabled", shell=True, capture_output=True)
            print(f"  [+] Stopped and disabled service: {service}")
        except Exception as e:
            print(f"  [-] Failed to stop/disable service {service}: {e}")

def disable_defender_task():
    print("[*] Disabling Windows Defender scheduled tasks...")
    tasks = [
        r"\Microsoft\Windows\Windows Defender\Windows Defender Scheduled Scan",
        r"\Microsoft\Windows\Windows Defender\Windows Defender Cache Maintenance",
        r"\Microsoft\Windows\Windows Defender\Windows Defender Cleanup",
        r"\Microsoft\Windows\Windows Defender\Windows Defender Verification",
    ]

    for task in tasks:
        try:
            subprocess.run(f"schtasks /Change /TN \"{task}\" /Disable", shell=True, capture_output=True)
            print(f"  [+] Disabled scheduled task: {task}")
        except Exception as e:
            print(f"  [-] Failed to disable scheduled task {task}: {e}")

def main():
    if not is_admin():
        print("[-] This script must be run as Administrator.")
        sys.exit(1)

    print("[*] Starting Microsoft Defender disable process...\n")

    disable_defender_powershell()
    print()
    disable_defender_registry()
    print()
    stop_defender_services()
    print()
    disable_defender_task()

    print("\n[*] Microsoft Defender disable attempts completed.")
    print("[*] A system reboot may be required for all changes to take effect.")

if __name__ == "__main__":
    main()
