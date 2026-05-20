#!/bin/bash
: <<'END'
Pregrade script for spectrogram-DWT image extraction lab.
It rebuilds grading state from the receiver's current files so checkwork
reflects the real extraction progress.
END

homedir=$1
destdir=$2
dbg=/tmp/audio-spectrogram-dwt-extract-pregrade.log

workdir="$homedir/$destdir/stego"
resultdir="$homedir/$destdir/.local/result"
result="$resultdir/spectrogram_dwt_extract_check.txt"
expected="$workdir/.expected_sha256"
image="$workdir/recovered_secret.png"

mkdir -p "$resultdir"
: > "$result"
echo "pregrade for $homedir/$destdir" > "$dbg"

pass() { echo "PASS_$1" >> "$result"; }
fail() { echo "FAIL_$1: $2" >> "$result"; }

if [ -s "$workdir/stego.wav" ]; then
    pass "AUDIO_RECEIVED"
else
    fail "AUDIO_RECEIVED" "stego.wav missing"
fi

if [ -s "$workdir/secret.key" ]; then
    pass "KEY_RECEIVED"
else
    fail "KEY_RECEIVED" "secret.key missing"
fi

if [ -s "$workdir/.dwt_signal_extracted" ]; then
    pass "DWT_SIGNAL_EXTRACTED"
else
    fail "DWT_SIGNAL_EXTRACTED" "DWT extraction marker missing"
fi

if [ -s "$workdir/.key_permutation_used" ]; then
    pass "KEY_PERMUTATION_USED"
else
    fail "KEY_PERMUTATION_USED" "key permutation marker missing"
fi

if [ -s "$image" ]; then
    pass "SECRET_IMAGE_RECOVERED"
else
    fail "SECRET_IMAGE_RECOVERED" "recovered_secret.png missing"
fi

if [ -s "$workdir/.recovered_image_viewed" ]; then
    pass "RECOVERED_IMAGE_VIEWED"
else
    fail "RECOVERED_IMAGE_VIEWED" "recovered image has not been viewed"
fi

if [ -s "$image" ] && [ -s "$expected" ]; then
    got=$(sha256sum "$image" | awk '{print $1}')
    want=$(tr -d ' \r\n' < "$expected")
    if [ "$got" = "$want" ]; then
        pass "RECOVERED_IMAGE_VALID"
    else
        fail "RECOVERED_IMAGE_VALID" "sha256 mismatch"
    fi
else
    fail "RECOVERED_IMAGE_VALID" "image or expected hash missing"
fi
