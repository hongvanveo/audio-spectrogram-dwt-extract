# Huong dan thuc hanh Lab 6: audio-spectrogram-dwt-extract

Lab 6 dung hai container `sender` va `receiver`. Sender gui file audio da giau tin `stego.wav` va key `secret.key`. Receiver se tach tin theo tung buoc: nhan file, tach tin hieu tu vung tan so cao bang DWT, dung key de dao hoan vi, sau do dung lai anh bi mat.

## Tai bai lab

```bash
imodule https://raw.githubusercontent.com/hongvanveo/audio-spectrogram-dwt-extract/main/imodule_audio-spectrogram-dwt-extract.tar
```

## Khoi dong

```bash
labtainer -r audio-spectrogram-dwt-extract
```

Khi duoc hoi email/student id, nhap ma sinh vien. Lab se chuan hoa ID sang chu IN HOA va checkwork chi cham ket qua cua ID dang dung.

## Quy trinh

```text
stego.wav + secret.key
-> extract_signal_task.py: DWT tren stego.wav, lay detail coefficients, tao hidden_signal.json
-> recover_image_task.py: dung key de dao hoan vi, tao recovered_secret.png
```

Moi task yeu cau sua file code de dien ten file dau vao roi moi chay. Sau moi task, chay `checkwork` de thay muc tuong ung chuyen sang `Y`.

## Task 1: Kiem tra sender

Trong terminal `sender`:

```bash
cd ~/stego
ls -l
cat README_sender.txt
./play_stego.sh
```

Sender can co `stego.wav` va `secret.key`.

## Task 2: Bat SSH tren receiver

Trong terminal `receiver`:

```bash
sudo service ssh start
systemctl status ssh
```

## Task 3: Gui file sang receiver

Trong terminal `sender`:

```bash
scp ~/stego/stego.wav ~/stego/secret.key ubuntu@receiver:~/stego/
ssh ubuntu@receiver "python3 ~/stego/refresh_status.py"
```

Trong terminal Labtainer:

```bash
checkwork
```

Can thay:

```text
Y - audio_received
Y - key_received
```

## Task 4: Tach tin hieu bi mat tu DWT

Trong terminal `receiver`:

```bash
cd ~/stego
nano extract_signal_task.py
```

Sua TODO:

```python
STEGO_FILE = "stego.wav"
KEY_FILE = "secret.key"
```

Chay:

```bash
python3 extract_signal_task.py
checkwork
```

Script nay phan ra `stego.wav` bang DWT, lay detail coefficients o muc cuoi va nhan lai voi he so `scaled` trong key de tao `hidden_signal.json`.

Can thay:

```text
Y - dwt_signal_extracted
```

## Task 5: Dung key de khoi phuc anh

Trong terminal `receiver`:

```bash
nano recover_image_task.py
```

Sua TODO:

```python
HIDDEN_SIGNAL = "hidden_signal.json"
KEY_FILE = "secret.key"
```

Chay:

```bash
python3 recover_image_task.py
checkwork
```

Script nay dung key de sinh lai thu tu permutation, dao hoan vi pixel va tao `recovered_secret.png`.

Can thay:

```text
Y - key_permutation_used
Y - secret_image_recovered
Y - recovered_image_valid
```

## Task 6: Mo anh da tach

Trong terminal `receiver`:

```bash
./view_recovered.sh
checkwork
```

Can thay:

```text
Y - recovered_image_viewed
```

## Ket qua cuoi cung

```text
Y - audio_received
Y - key_received
Y - dwt_signal_extracted
Y - key_permutation_used
Y - secret_image_recovered
Y - recovered_image_viewed
Y - recovered_image_valid
```

Ket thuc:

```bash
stoplab audio-spectrogram-dwt-extract
```
