import os
import sys
import platform
import subprocess
from pathlib import Path

def check_windows_tasks():
    print("\n[+] Scheduled Tasks:")
    try:
        output = subprocess.check_output(['schtasks', '/query', '/fo', 'LIST', '/v'], text=True)
        print(output.strip())
    except Exception as e:
        print(f"[-] Error reading scheduled tasks: {e}")

    print("\n[+] Common Run Keys (Registry Persistence):")
    try:
        import winreg
        keys = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]
        for hive, path in keys:
            try:
                with winreg.OpenKey(hive, path) as key:
                    print(f"\n[>] Registry Path: {path}")
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            print(f"  {name} = {value}")
                            i += 1
                        except OSError:
                            break  # Reached end of values
            except FileNotFoundError:
                print(f"  (Registry path not found: {path})")
    except ImportError:
        print("[-] winreg module not available")

    print("\n[+] Startup Folder Items:")
    startup_paths = [
        Path(os.getenv("APPDATA")) / "Microsoft\\Windows\\Start Menu\\Programs\\Startup",
        Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Startup")
    ]
    for path in startup_paths:
        print(f"\n{path}:")
        if path.exists():
            files = list(path.glob("*"))
            if files:
                for f in files:
                    print(f"  - {f.name}")
            else:
                print("  (No items found)")
        else:
            print("  (Path not found)")

def check_unix_cron_jobs():
    print("\n[+] User Crontab:")
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT, text=True)
        print(output.strip())
    except subprocess.CalledProcessError:
        print("  (No user crontab or access denied)")

    print("\n[+] System-Wide Cron Jobs (/etc/cron*):")
    cron_dirs = ["/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly", "/etc/cron.monthly", "/etc/cron.weekly"]
    for dir in cron_dirs:
        print(f"\n{dir}:")
        if os.path.isdir(dir):
            files = os.listdir(dir)
            if files:
                for file in files:
                    print(f"  - {file}")
            else:
                print("  (Empty)")
        else:
            print("  (Directory not found)")

    print("\n[+] System Crontab (/etc/crontab):")
    try:
        with open("/etc/crontab", "r") as f:
            print(f.read().strip())
    except FileNotFoundError:
        print("  (Not found)")

def main():
    os_type = platform.system()
    print(f"[+] Detected OS: {os_type}")

    if os_type == "Windows":
        check_windows_tasks()
    elif os_type in ("Linux", "Darwin"):
        check_unix_cron_jobs()
    else:
        print("[-] Unsupported OS.")

if __name__ == "__main__":
    main()
