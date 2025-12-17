import qrcode as qr

link = "newtonspace.netlify.app"

img = qr.make(link)
img.save("prof.jpeg")