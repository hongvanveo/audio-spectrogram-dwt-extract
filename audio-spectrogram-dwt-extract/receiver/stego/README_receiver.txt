Receiver can nhan stego.wav va secret.key tu sender, sau do tach theo tung buoc.

Neu muon checkwork cap nhat ngay sau khi sender gui file, chay:

  python3 refresh_status.py

Buoc 1 - tach tin hieu mien thoi gian tu he so tan so cao DWT:

  cd ~/stego
  nano extract_signal_task.py

Sua:

  STEGO_FILE = "stego.wav"
  KEY_FILE = "secret.key"

Chay:

  python3 extract_signal_task.py

Buoc 2 - dung key de hoan vi nguoc va dung lai anh:

  nano recover_image_task.py

Sua:

  HIDDEN_SIGNAL = "hidden_signal.json"
  KEY_FILE = "secret.key"

Chay:

  python3 recover_image_task.py

Mo truc tiep anh da tach:

  ./view_recovered.sh

Ket qua dung la file recovered_secret.png.
