#!/usr/bin/env python3
import argparse
import hashlib
import math
import os
import random
import struct
import wave
import zlib
from array import array


def home_path(*parts):
    base = os.environ.get("HOME") or os.path.expanduser("~")
    return os.path.join(base, *parts)


RESULT = home_path(".local", "result", "spectrogram_dwt_extract_check.txt")


def mark(token):
    os.makedirs(os.path.dirname(RESULT), exist_ok=True)
    existing = set()
    if os.path.exists(RESULT):
        with open(RESULT, "r", encoding="utf-8") as handle:
            existing = {line.strip() for line in handle if line.strip()}
    existing.add(token)
    with open(RESULT, "w", encoding="utf-8") as handle:
        handle.write("\n".join(sorted(existing)) + "\n")


def parse_key_file(path):
    meta = {}
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"bad key line: {line}")
            key, value = line.split("=", 1)
            meta[key.strip().upper()] = value.strip()
    required = ["KEY", "WIDTH", "HEIGHT", "N_SAMPLES", "N_EMBEDDED", "SCALED"]
    missing = [name for name in required if name not in meta]
    if missing:
        raise ValueError("secret.key missing: " + ", ".join(missing))
    return {
        "key": int(meta["KEY"]),
        "width": int(meta["WIDTH"]),
        "height": int(meta["HEIGHT"]),
        "n_samples": int(meta["N_SAMPLES"]),
        "n_embedded": int(meta["N_EMBEDDED"]),
        "scaled": float(meta["SCALED"]),
        "wavelet": meta.get("WAVELET", "haar"),
    }


def read_wav(path):
    with wave.open(path, "rb") as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
    if params.sampwidth != 2 or params.nchannels != 1:
        raise ValueError("stego.wav must be mono PCM16")
    samples = array("h")
    samples.frombytes(frames)
    return params, [float(x) for x in samples]


def haar_dwt_level(samples):
    approx = []
    detail = []
    inv = 1.0 / math.sqrt(2.0)
    for i in range(0, len(samples), 2):
        a = samples[i]
        b = samples[i + 1] if i + 1 < len(samples) else samples[i]
        approx.append((a + b) * inv)
        detail.append((a - b) * inv)
    return approx, detail


def multilevel_haar_dwt(samples, n_embedded):
    level = max(1, int(math.floor(math.log2(max(2, len(samples) / max(1, n_embedded))))))
    approx = list(samples)
    details = []
    for _ in range(level):
        approx, detail = haar_dwt_level(approx)
        details.append(detail)
    return details, level


def inverse_permutation(values, key):
    order = list(range(len(values)))
    rng = random.Random(key)
    rng.shuffle(order)
    recovered = [0] * len(values)
    for encrypted_index, original_index in enumerate(order):
        recovered[original_index] = values[encrypted_index]
    with open(".key_permutation_used", "w", encoding="utf-8") as handle:
        handle.write(f"key={key}\n")
        handle.write(f"values={len(values)}\n")
    mark("PASS_KEY_PERMUTATION_USED")
    return recovered


def write_png_gray(path, width, height, pixels):
    raw_rows = []
    for y in range(height):
        start = y * width
        row = bytes(max(0, min(255, int(v))) for v in pixels[start:start + width])
        raw_rows.append(b"\x00" + row)
    raw = b"".join(raw_rows)

    def chunk(name, data):
        body = name + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as handle:
        handle.write(png)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def extract(args):
    if not os.path.exists(args.stego):
        raise FileNotFoundError(args.stego)
    if not os.path.exists(args.keyfile):
        raise FileNotFoundError(args.keyfile)
    mark("PASS_AUDIO_RECEIVED")
    mark("PASS_KEY_RECEIVED")

    meta = parse_key_file(args.keyfile)
    params, samples = read_wav(args.stego)
    audio = samples[:meta["n_samples"]]
    details, level = multilevel_haar_dwt(audio, meta["n_embedded"])
    high_frequency = details[-1][:meta["n_embedded"]]
    hidden_signal = [value * meta["scaled"] for value in high_frequency]
    encrypted_pixels = [255 if value >= 0 else 0 for value in hidden_signal]

    with open(".dwt_signal_extracted", "w", encoding="utf-8") as handle:
        handle.write(f"wavelet={meta['wavelet']}\n")
        handle.write(f"levels={level}\n")
        handle.write(f"coefficients={len(high_frequency)}\n")
    mark("PASS_DWT_SIGNAL_EXTRACTED")

    recovered_pixels = inverse_permutation(encrypted_pixels, meta["key"])
    expected_count = meta["width"] * meta["height"]
    if len(recovered_pixels) < expected_count:
        raise ValueError("not enough recovered pixels")
    write_png_gray(args.out, meta["width"], meta["height"], recovered_pixels[:expected_count])
    mark("PASS_SECRET_IMAGE_RECOVERED")

    expected_hash_path = ".expected_sha256"
    if os.path.exists(expected_hash_path):
        with open(expected_hash_path, "r", encoding="utf-8") as handle:
            expected = handle.read().strip()
        if sha256_file(args.out) == expected:
            mark("PASS_RECOVERED_IMAGE_VALID")

    print(f"stego={args.stego}")
    print(f"key={meta['key']}")
    print(f"dwt_levels={level}")
    print(f"recovered={args.out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["extract"])
    parser.add_argument("--stego", required=True)
    parser.add_argument("--keyfile", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    extract(args)


if __name__ == "__main__":
    main()
