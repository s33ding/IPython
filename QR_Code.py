#source>>>https://youtu.be/l4ugfcj7qrI
import qrcode
link = input("LINK: ")
img = qrcode.make(link)
img.save('QR_Code.png')
