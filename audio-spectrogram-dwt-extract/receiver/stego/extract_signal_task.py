#!/usr/bin/env python3
import json
import os

from spectrogram_dwt_extract import mark, multilevel_haar_dwt, parse_key_file, read_wav


def get_inputs():
    # TODO: dien ten file audio stego ma receiver nhan duoc tu sender.
    STEGO_FILE = "TODO_STEGO_FILENAME"

    # TODO: dien ten file key ma sender gui kem theo audio stego.
    KEY_FILE = "TODO_KEY_FILENAME"

    OUTPUT_SIGNAL = "hidden_signal.json"
    if "TODO" in STEGO_FILE or "TODO" in KEY_FILE:
        raise SystemExit("Hay mo extract_signal_task.py va dien stego.wav va secret.key truoc khi chay.")
    return STEGO_FILE, KEY_FILE, OUTPUT_SIGNAL


def main():
    stego_file, key_file, output_signal = get_inputs()
    if not os.path.exists(stego_file):
        raise FileNotFoundError(stego_file)
    if not os.path.exists(key_file):
        raise FileNotFoundError(key_file)

    mark("PASS_AUDIO_RECEIVED")
    mark("PASS_KEY_RECEIVED")

    meta = parse_key_file(key_file)
    _, samples = read_wav(stego_file)
    audio = samples[:meta["n_samples"]]
    details, level = multilevel_haar_dwt(audio, meta["n_embedded"])
    high_frequency = details[-1][:meta["n_embedded"]]
    hidden_signal = [value * meta["scaled"] for value in high_frequency]

    with open(output_signal, "w", encoding="utf-8") as handle:
        json.dump(
            {
                "stego": stego_file,
                "key_file": key_file,
                "key": meta["key"],
                "width": meta["width"],
                "height": meta["height"],
                "n_embedded": meta["n_embedded"],
                "scaled": meta["scaled"],
                "wavelet": meta["wavelet"],
                "dwt_levels": level,
                "signal": hidden_signal,
            },
            handle,
        )

    with open(".dwt_signal_extracted", "w", encoding="utf-8") as handle:
        handle.write(f"wavelet={meta['wavelet']}\n")
        handle.write(f"levels={level}\n")
        handle.write(f"coefficients={len(high_frequency)}\n")
        handle.write(f"source={stego_file}\n")

    mark("PASS_DWT_SIGNAL_EXTRACTED")
    print(f"stego={stego_file}")
    print(f"keyfile={key_file}")
    print(f"dwt_levels={level}")
    print(f"hidden_signal={output_signal}")


if __name__ == "__main__":
    main()
