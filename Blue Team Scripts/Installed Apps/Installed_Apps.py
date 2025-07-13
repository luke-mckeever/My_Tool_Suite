import os
import hashlib
import platform
import winreg
from pathlib import Path

def get_installed_apps_windows():
    apps = []
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]

    for hive, path in reg_paths:
        try:
            with winreg.OpenKey(hive, path) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0] if "InstallLocation" in [winreg.EnumValue(subkey, j)[0] for j in range(winreg.QueryInfoKey(subkey)[1])] else None
                            if name:
                                apps.append((name, install_location))
                    except (OSError, IndexError, FileNotFoundError):
                        continue
        except FileNotFoundError:
            continue
    return apps

def hash_file(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def hash_directory(folder):
    hashes = []
    folder_path = Path(folder)
    if not folder_path.exists() or not folder_path.is_dir():
        return []
    for file in folder_path.rglob("*"):
        if file.is_file():
            hash_val = hash_file(file)
            if hash_val:
                hashes.append((str(file), hash_val))
    return hashes

def main():
    if platform.system() != "Windows":
        print("[-] This script currently supports Windows only.")
        return

    apps = get_installed_apps_windows()
    print(f"[+] Found {len(apps)} installed applications\n")

    for name, location in apps:
        print(f"\n=== {name} ===")
        if location and Path(location).exists():
            print(f"Install Location: {location}")
            hashes = hash_directory(location)
            if hashes:
                for file, h in hashes[:3]:  # limit to 3 files per app to avoid overload
                    print(f"  {file}:\n    SHA256: {h}")
            else:
                print("  No readable files to hash.")
        else:
            print("  Install location not available or does not exist.")

    print("\n[✓] Application hash collection complete.")

if __name__ == "__main__":
    main()
