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
-> extract_signal.py: DWT tren stego.wav, lay detail coefficients, tao hidden_signal.json
-> recover_image.py: dung key de dao hoan vi, tao recovered_secret.png
```

Moi task yeu cau sua file code de dien ten file dau vao roi moi chay. Sinh vien chi can kiem tra lenh tao dung file dau ra cua task do; khong can chay `checkwork` sau tung task.

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

Trong terminal `receiver`, kiem tra:

```bash
ls -l ~/stego/stego.wav ~/stego/secret.key
```

## Task 4: Tach tin hieu bi mat tu DWT

Trong terminal `receiver`:

```bash
cd ~/stego
nano extract_signal.py
```

Sua TODO:

```python
STEGO_FILE = "stego.wav"
KEY_FILE = "secret.key"
```

Chay:

```bash
python3 extract_signal.py
ls -l hidden_signal.json
```

Script nay phan ra `stego.wav` bang DWT, lay detail coefficients o muc cuoi va nhan lai voi he so `scaled` trong key de tao `hidden_signal.json`.

## Task 5: Dung key de khoi phuc anh

Trong terminal `receiver`:

```bash
nano recover_image.py
```

Sua TODO:

```python
HIDDEN_SIGNAL = "hidden_signal.json"
KEY_FILE = "secret.key"
```

Chay:

```bash
python3 recover_image.py
ls -l recovered_secret.png
```

Script nay dung key de sinh lai thu tu permutation, dao hoan vi pixel va tao `recovered_secret.png`.

## Task 6: Mo anh da tach

Trong terminal `receiver`:

```bash
./view_recovered.sh
```

Anh `recovered_secret.png` can mo duoc bang cua so xem anh binh thuong.

## Ket qua cuoi cung

Sau khi lam xong tat ca task, chay trong terminal Labtainer:

```bash
checkwork
```

Ket qua dung:

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
