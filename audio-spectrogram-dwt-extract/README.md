# Lab 6: Audio Spectrogram DWT Extraction

Lab nay mo phong ben nhan trong quy trinh image-in-audio steganography.
Sender gui `stego.wav` va `secret.key`; receiver dung DWT de lay he so tan so cao,
nhan lai theo he so scale, dao hoan vi bang key va tao lai anh bi mat.

Pipeline:

`stego.wav + secret.key -> DWT high-frequency detail -> hidden signal -> inverse permutation -> recovered_secret.png`

Phuong phap bam theo y tuong retrieving trong repo
`haoyuhsu/Image-in-Audio-Steganography`: lay detail coefficients o muc DWT cuoi,
nhan lai bang `scaled`, sau do dung key lam seed de dao permutation.

Khi `labtainer` hoi e-mail/student id, sinh vien nhap ma cua minh. He thong se
chuan hoa ma do thanh chu IN HOA va ghi nho ID gan nhat cho lan mo lab sau.
`checkwork` chi hien va cham ket qua cua dung ID dang duoc su dung cho lab hien tai.

## Chay nhanh

Trong receiver:

```bash
sudo service ssh start
```

Trong sender:

```bash
./play_stego.sh
scp ~/stego/stego.wav ~/stego/secret.key ubuntu@receiver:~/stego/
```

Trong receiver:

```bash
cd ~/stego
nano extract_task.py
python3 extract_task.py
./view_recovered.sh
checkwork
```
