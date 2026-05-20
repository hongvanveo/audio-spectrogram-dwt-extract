#!/usr/bin/env python3
import subprocess
import sys


def get_inputs():
    # TODO: dien ten file audio stego ma receiver nhan duoc tu sender.
    STEGO_FILE = "TODO_STEGO_FILENAME"

    # TODO: dien ten file key ma sender gui kem theo audio stego.
    KEY_FILE = "TODO_KEY_FILENAME"

    output_image = "recovered_secret.png"
    if "TODO" in STEGO_FILE or "TODO" in KEY_FILE:
        raise SystemExit("Hay mo extract_task.py va dien ten stego.wav va secret.key truoc khi chay.")
    return STEGO_FILE, KEY_FILE, output_image


def main():
    stego_file, key_file, output_image = get_inputs()
    cmd = [
        "python3",
        "spectrogram_dwt_extract.py",
        "extract",
        "--stego",
        stego_file,
        "--keyfile",
        key_file,
        "--out",
        output_image,
    ]
    subprocess.run(cmd, check=True)
    print(f"Da tach anh bi mat ra {output_image} tu {stego_file} bang key trong {key_file}.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
