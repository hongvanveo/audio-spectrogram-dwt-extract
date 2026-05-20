#!/usr/bin/env python3
import hashlib
import os


BASE = os.path.join(os.environ.get("HOME", os.path.expanduser("~")), "stego")
RESULT = os.path.join(os.environ.get("HOME", os.path.expanduser("~")), ".local", "result", "spectrogram_dwt_extract_check.txt")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    tokens = []
    stego = os.path.join(BASE, "stego.wav")
    key = os.path.join(BASE, "secret.key")
    image = os.path.join(BASE, "recovered_secret.png")
    expected = os.path.join(BASE, ".expected_sha256")
    if os.path.getsize(stego) > 0 if os.path.exists(stego) else False:
        tokens.append("PASS_AUDIO_RECEIVED")
    if os.path.getsize(key) > 0 if os.path.exists(key) else False:
        tokens.append("PASS_KEY_RECEIVED")
    if os.path.exists(os.path.join(BASE, ".dwt_signal_extracted")):
        tokens.append("PASS_DWT_SIGNAL_EXTRACTED")
    if os.path.exists(os.path.join(BASE, ".key_permutation_used")):
        tokens.append("PASS_KEY_PERMUTATION_USED")
    if os.path.getsize(image) > 0 if os.path.exists(image) else False:
        tokens.append("PASS_SECRET_IMAGE_RECOVERED")
    if os.path.exists(os.path.join(BASE, ".recovered_image_viewed")):
        tokens.append("PASS_RECOVERED_IMAGE_VIEWED")
    if os.path.exists(image) and os.path.exists(expected):
        with open(expected, "r", encoding="utf-8") as handle:
            wanted = handle.read().strip()
        if sha256_file(image) == wanted:
            tokens.append("PASS_RECOVERED_IMAGE_VALID")
    with open(RESULT, "w", encoding="utf-8") as handle:
        handle.write("\n".join(tokens) + ("\n" if tokens else ""))


if __name__ == "__main__":
    main()
