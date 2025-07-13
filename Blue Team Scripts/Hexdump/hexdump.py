import sys

def hex_dump(file_path, bytes_per_line=16):
    try:
        with open(file_path, 'rb') as f:
            offset = 0
            while True:
                chunk = f.read(bytes_per_line)
                if not chunk:
                    break
                hex_chunk = ' '.join(f"{byte:02X}" for byte in chunk)
                ascii_chunk = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk)
                print(f"{offset:08X}  {hex_chunk:<{bytes_per_line*3}}  {ascii_chunk}")
                offset += bytes_per_line
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python hex_viewer.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    hex_dump(file_path)

if __name__ == "__main__":
    main()
