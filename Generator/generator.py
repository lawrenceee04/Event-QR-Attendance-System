import pandas as pd
import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
                                                  
# File/Variable Names
name = "QR Codes/qrCode{number}.jpg"

df = pd.read_csv("config_files/guestList.csv", index_col = False)
col_QrData = df["qrValues"]
col_FirstName= df["firstName"]

for i in range(len(col_QrData)):
    img = qrcode.make(col_QrData[i])
    type(img)  # qrcode.image.pil.PilImage
    index = i + 1
    img.save(name.format(number = index))