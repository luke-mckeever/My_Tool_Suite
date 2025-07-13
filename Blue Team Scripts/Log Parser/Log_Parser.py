import win32evtlog
import win32evtlogutil
import win32con
import datetime
from collections import Counter

# Event IDs to monitor (Windows Security Log)
EVENT_IDS = {
    4624: "Successful Logon",
    4625: "Failed Logon",
    4634: "Logoff",
    4647: "User Initiated Logoff",
    4720: "User Account Created",
    4722: "User Account Enabled",
    4723: "Password Change Attempt",
    4724: "Password Reset",
    4725: "User Account Disabled",
    4726: "User Account Deleted",
    4740: "Account Locked Out",
    4672: "Admin Logon",
    1102: "Audit Log Cleared"
}

def get_security_logs(server="localhost"):
    hand = win32evtlog.OpenEventLog(server, "Security")
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    event_data = []

    print(f"[+] Reading the last {total} security events...")

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break
        for event in events:
            if event.EventID in EVENT_IDS:
                timestamp = event.TimeGenerated.Format()  # readable format
                username = event.StringInserts[5] if len(event.StringInserts) >= 6 else "N/A"
                ip_address = event.StringInserts[18] if len(event.StringInserts) >= 19 else "N/A"
                event_data.append({
                    "Time": timestamp,
                    "EventID": event.EventID,
                    "EventType": EVENT_IDS[event.EventID],
                    "User": username,
                    "SourceIP": ip_address
                })

    return event_data

def summarize(events):
    print("\n=== Summary of Security Events ===")
    counts = Counter(event["EventType"] for event in events)
    for event_type, count in counts.items():
        print(f"{event_type}: {count}")

    print("\n=== Recent Events (Last 10) ===")
    for event in events[:10]:
        print(f"{event['Time']} | {event['EventType']} | User: {event['User']} | IP: {event['SourceIP']}")

def main():
    try:
        logs = get_security_logs()
        if logs:
            summarize(logs)
        else:
            print("[-] No relevant security logs found.")
    except Exception as e:
        print(f"[!] Error while parsing security logs: {e}")

if __name__ == "__main__":
    main()
