import PIL
import qrcode
import random
import ImageFont
import ImageDraw


def label(i, string, img):

    sz = img.size
    
    width1 = sz[0]
    #width2 = sz[0]*17/22
    #width2 = sz[0]*6/4
    #width2 = sz[0]*7/5
    width2 = sz[0]*13/10
    
    img2 = PIL.Image.new("RGB", (width2, sz[1]), "white")
    
    img2.paste(img, (width2 - width1,0))

    font = ImageFont.truetype("UbuntuMono-R.ttf", 15)

    draw = ImageDraw.Draw(img2)

    draw.text((0,0), string, font=font, fill="rgb(0,0,0)")

    img2.save("label{}.png".format(i))
   

n = 128

random.seed()
a = random.randint(0,1000)

strings = ["girl","boy"]
index = [a % 2, (a+1) % 2]
codes = [random.randint(0,2**n), random.randint(0,2**n)]
imgs = [qrcode.make(codes[0]), qrcode.make(codes[1])]



for i in range(2):
    j = index[i]

    label(i, strings[j], imgs[j])



