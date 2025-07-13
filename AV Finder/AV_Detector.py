import wmi
import psutil

# Known AV and EDR process names (common executables)
KNOWN_AV_EDR_PROCESSES = {
    "Microsoft Defender": ["MsMpEng.exe"],
    "McAfee": ["mcshield.exe", "mfemms.exe", "mcafee.exe"],
    "Symantec": ["ccSvcHst.exe", "smc.exe"],
    "CrowdStrike": ["csagent.exe", "falcon.exe"],
    "Carbon Black": ["cb.exe", "cbdefense.exe", "cbsensor.exe"],
    "SentinelOne": ["SentinelCtl.exe", "SentinelAgent.exe"],
    "Sophos": ["SophosUI.exe", "SavService.exe"],
    "Trend Micro": ["TmListen.exe", "PccNTMon.exe"],
    "Kaspersky": ["avp.exe"],
    "Bitdefender": ["vsserv.exe"],
    # Add more as needed
}

def get_installed_antivirus():
    antivirus_list = []
    try:
        c = wmi.WMI(namespace="root\\SecurityCenter2")
        for av in c.AntiVirusProduct():
            antivirus_list.append(av.displayName)
    except Exception as e:
        print(f"Error accessing WMI: {e}")
    return antivirus_list

def scan_processes_for_av_edr():
    found_agents = set()
    for proc in psutil.process_iter(['name']):
        try:
            pname = proc.info['name']
            if not pname:
                continue
            for av_name, proc_names in KNOWN_AV_EDR_PROCESSES.items():
                if pname.lower() in (p.lower() for p in proc_names):
                    found_agents.add(av_name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return list(found_agents)

if __name__ == "__main__":
    print("Scanning for installed antivirus products via WMI...")
    av_products = get_installed_antivirus()
    if av_products:
        print("Detected Antivirus Products (WMI):")
        for av in av_products:
            print(f"- {av}")
    else:
        print("No antivirus products found via WMI or unable to query.")

    print("\nScanning running processes for known AV/EDR agents...")
    av_edr_agents = scan_processes_for_av_edr()
    if av_edr_agents:
        print("Detected AV/EDR agents running as processes:")
        for agent in av_edr_agents:
            print(f"- {agent}")
    else:
        print("No known AV/EDR agents detected in running processes.")
