import argparse
import requests
import re
import sys

def identify_input_type(input_str):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if re.fullmatch(email_regex, input_str):
        return "email"
    elif " " in input_str.strip():
        return "full_name"
    else:
        return "username"

def check_username_platforms(username):
    platforms = {
        # General & Popular
        "X (Twitter)": f"https://twitter.com/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "LinkedIn": f"https://www.linkedin.com/in/{username}",
        "Tumblr": f"https://{username}.tumblr.com",
        "Flickr": f"https://www.flickr.com/people/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Medium": f"https://medium.com/@{username}",
        "DeviantArt": f"https://{username}.deviantart.com",
        "VK": f"https://vk.com/{username}",
        "Mastodon": f"https://mastodon.social/@{username}",
        "Gab": f"https://gab.com/{username}",
        "Truth Social": f"https://truthsocial.com/@{username}",

        # Gaming
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Roblox": f"https://www.roblox.com/users/{username}/profile",  # usually numeric userID
        "Speedrun.com": f"https://www.speedrun.com/user/{username}",
        "Chess.com": f"https://www.chess.com/member/{username}",

        # Developer & Technical
        "GitHub": f"https://github.com/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Stack Overflow": f"https://stackoverflow.com/users/{username}",
        "HackerOne": f"https://hackerone.com/{username}",
        "TryHackMe": f"https://tryhackme.com/p/{username}",
        "Hack The Box": f"https://app.hackthebox.com/profile/{username}",
        "Replit": f"https://replit.com/@{username}",
        "Dev.to": f"https://dev.to/{username}",

        # Other
        "Spotify": f"https://open.spotify.com/user/{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}"
    }

    found = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OSINT-Tool/1.0)"
    }

    for platform, url in platforms.items():
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                found[platform] = url
        except requests.RequestException:
            pass  # Ignore network errors

    return found

def main():
    parser = argparse.ArgumentParser(description="Check if a username exists across many social platforms.")
    parser.add_argument("input", help="Username, email address, or full name to search for")
    args = parser.parse_args()

    user_input = args.input.strip()
    input_type = identify_input_type(user_input)

    if input_type == "username":
        print(f"[+] Searching for username: {user_input}")
        results = check_username_platforms(user_input)
        if results:
            print("[+] Accounts found:")
            for platform, url in results.items():
                print(f"  - {platform}: {url}")
        else:
            print("[-] No accounts found with that username.")
    elif input_type == "email":
        print("[-] Email search not implemented. Consider HaveIBeenPwned or Gravatar APIs.")
    elif input_type == "full_name":
        print("[-] Full name search not implemented. Consider search engine integration.")
    else:
        print("[-] Could not determine input type.")

if __name__ == "__main__":
    main()
