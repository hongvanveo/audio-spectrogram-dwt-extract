import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LAB = ROOT / "audio-spectrogram-dwt-extract"
OUT = ROOT / "imodule_audio-spectrogram-dwt-extract.tar"


def add_tree(tar, path, arcname):
    if path.name == "__pycache__":
        return
    info = tar.gettarinfo(str(path), arcname)
    if path.is_dir():
        info.mode = 0o755
        tar.addfile(info)
        for child in sorted(path.iterdir(), key=lambda p: p.name):
            add_tree(tar, child, f"{arcname}/{child.name}")
        return
    if path.name == "pregrade.sh" or path.suffix == ".py":
        info.mode = 0o755
    elif path.name == "id_ed25519":
        info.mode = 0o600
    elif path.name in {"authorized_keys", "config"}:
        info.mode = 0o600
    else:
        info.mode = 0o644
    with path.open("rb") as handle:
        tar.addfile(info, handle)


def main():
    if OUT.exists():
        OUT.unlink()
    with tarfile.open(OUT, "w") as tar:
        add_tree(tar, LAB, LAB.name)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
