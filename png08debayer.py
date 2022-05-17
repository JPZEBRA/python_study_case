# 趣味のPython学習　Project 02-01
# Python PNG08 DEBAYER
# ばーじょん 1.0.2

ver = "1.0.2"

from io import BytesIO

from PIL import Image
from PIL import ImageFile

def rdd(img,x,y) :
    if x < 0 :
        return 0
    if y < 0 :
        return 0
    if x >= img.size[0] :
        return 0
    if y >= img.size[1] :
        return 0
    return img.getpixel((x,y))

def debayer00(img,x,y) :

    dt00 = rdd(img,x,y)
    return (dt00,dt00,dt00)

def debayer2x2RGGB(img,x,y) :

    xx = (x // 2)*2
    yy = (y // 2)*2

    dt01 = rdd(img,xx+0,yy+0)
    dt02 = rdd(img,xx+1,yy+0)
    dt03 = rdd(img,xx+0,yy+1)
    dt04 = rdd(img,xx+1,yy+1)

    red = dt01
    grn = (dt02 + dt03) // 2
    blu = dt04

    return (red,grn,blu)

def debayer3x3RGGB(img,x,y) :

    dt11 = rdd(img,x-1,y-1)
    dt12 = rdd(img,x+0,y-1)
    dt13 = rdd(img,x+1,y-1)

    dt21 = rdd(img,x-1,y+0)
    dt22 = rdd(img,x+0,y+0)
    dt23 = rdd(img,x+1,y+0)

    dt31 = rdd(img,x-1,y+1)
    dt32 = rdd(img,x+0,y+1)
    dt33 = rdd(img,x+1,y+1)

    if x%2==0 and y%2==0 :
        red = dt22
        grn = (dt12+dt21+dt23+dt32)//4
        blu = (dt11+dt13+dt31+dt33)//4
    if x%2==0 and y%2==1 :
        red = (dt12+dt32)//2
        grn = dt22
        blu = (dt21+dt23)//2
    if x%2==1 and y%2==0 :
        red = (dt21+dt23)//2
        grn = dt22
        blu = (dt12+dt32)//2
    if x%2==1 and y%2==1 :
        red = (dt11+dt13+dt31+dt33)//4
        blu = dt22
        grn = (dt12+dt21+dt23+dt32)//4

    return (red,grn,blu)

print(f"*** PNG08-GRAY to TRUE-COLOR CONVERTER VERSION {ver} ***")
print("\nSELECT PNG08 GRAY SCALE FILE\n")

while len( fnm := input("file : ") ) > 0 :

    try :

        img_src = Image.open(fnm,'r')
        img_src.verify()

    except FileNotFoundError:
        print(f"{fnm} : not found !")

    except PIL.UnidentifiedImageError:
        print(f"{fnm} : type error !")

    else :

        print(f"{fnm} : read OK !")

        wd = img_src.size[0]
        ht = img_src.size[1]
        md = img_src.mode
        print(f"W:{wd} H:{ht} M:{md}")

        if md != "L" :
            print(f"{fnm} : not glay scale.")
            continue

        print("*** CONVERT MODE ***")
        print("1: GRAY")
        print("2: RGGB 2x2")
        print("3: RGGB 3x3")

        while True :
            md = int(input("MODE :"))
            if 1 <= md and md <= 3 :
                break


#       RE OPEN AS A BINARY

        with open(fnm,'rb') as f :
            data = f.read()
            img_src = Image.open(BytesIO(data))

#       CONVERT DATA
        img_cv = Image.new('RGB',img_src.size)

        for y in range(img_src.size[1]) :
            for x in range(img_src.size[0]) :
                if md == 1 :
                    px  = debayer00(img_src,x,y)
                if md == 2 :
                    px  = debayer2x2RGGB(img_src,x,y)
                if md == 3 :
                    px  = debayer3x3RGGB(img_src,x,y)
                img_cv.putpixel((x,y),px)


        fno = fnm + ".debayered-" + str(md) + ".png"
        print(f"WRITE OUT : {fno}")
        img_cv.save(fno)

        print("*** DONE ***")


