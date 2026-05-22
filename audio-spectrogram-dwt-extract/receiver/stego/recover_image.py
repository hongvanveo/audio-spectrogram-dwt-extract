#!/usr/bin/env python3
import json
import os

from spectrogram_dwt_extract import (
    inverse_permutation,
    mark,
    parse_key_file,
    sha256_file,
    write_png_gray,
)


def get_inputs():
    # Dien file tin hieu da tach tu extract_signal.py vao chuoi rong ben duoi.
    HIDDEN_SIGNAL = ""

    # Dien ten file key da nhan tu sender vao chuoi rong ben duoi.
    KEY_FILE = ""

    OUTPUT_IMAGE = "recovered_secret.png"
    if not HIDDEN_SIGNAL.strip() or not KEY_FILE.strip():
        raise SystemExit("Hay mo recover_image.py va dien hidden_signal.json va secret.key vao cac chuoi rong truoc khi chay.")
    return HIDDEN_SIGNAL, KEY_FILE, OUTPUT_IMAGE


def main():
    hidden_signal_file, key_file, output_image = get_inputs()
    if not os.path.exists(hidden_signal_file):
        raise FileNotFoundError(hidden_signal_file)
    if not os.path.exists(key_file):
        raise FileNotFoundError(key_file)

    meta = parse_key_file(key_file)
    with open(hidden_signal_file, "r", encoding="utf-8") as handle:
        hidden_info = json.load(handle)

    if hidden_info["width"] != meta["width"] or hidden_info["height"] != meta["height"]:
        raise ValueError("hidden_signal.json khong khop voi secret.key")

    hidden_signal = hidden_info["signal"]
    encrypted_pixels = [255 if value >= 0 else 0 for value in hidden_signal]
    recovered_pixels = inverse_permutation(encrypted_pixels, meta["key"])
    expected_count = meta["width"] * meta["height"]
    if len(recovered_pixels) < expected_count:
        raise ValueError("khong du pixel de khoi phuc anh")

    write_png_gray(output_image, meta["width"], meta["height"], recovered_pixels[:expected_count])
    mark("PASS_SECRET_IMAGE_RECOVERED")

    expected_hash_path = ".expected_sha256"
    if os.path.exists(expected_hash_path):
        with open(expected_hash_path, "r", encoding="utf-8") as handle:
            expected = handle.read().strip()
        if sha256_file(output_image) == expected:
            mark("PASS_RECOVERED_IMAGE_VALID")

    print(f"hidden_signal={hidden_signal_file}")
    print(f"key={meta['key']}")
    print(f"recovered={output_image}")


if __name__ == "__main__":
    main()
