Sender co san hai file can gui cho receiver:

  stego.wav
  secret.key

Nghe truc tiep audio stego:

  ./play_stego.sh

Sau khi receiver bat ssh, gui hai file bang lenh:

  scp ~/stego/stego.wav ~/stego/secret.key ubuntu@receiver:~/stego/
  ssh ubuntu@receiver "python3 ~/stego/refresh_status.py"
