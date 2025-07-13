import pyperclip

def dump_clipboard(filename="clipboard_dump.txt"):
    try:
        clipboard_content = pyperclip.paste()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(clipboard_content)
        print(f"Clipboard content dumped to {filename}")
    except Exception as e:
        print(f"Failed to dump clipboard content: {e}")

if __name__ == "__main__":
    dump_clipboard()
