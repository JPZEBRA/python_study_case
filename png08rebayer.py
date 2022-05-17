# 趣味のPython学習　Project 02-02
# Python PNG08 REBAYER
# ばーじょん 1.0.5

ver = "1.0.5"

from io import BytesIO

from PIL import Image
from PIL import ImageFile

def rdd(img,x,y) :
    if x < 0 :
        return (0,0,0)
    if y < 0 :
        return (0,0,0)
    if x >= img.size[0] :
        return (0,0,0)
    if y >= img.size[1] :
        return (0,0,0)
    return img.getpixel((x,y))

def rebayer00RGGB(img,x,y) :

    rgb = rdd(img,x,y)

    dt11 = (rgb[0]+rgb[1]+rgb[2]) // 3

    return (dt11,dt11,dt11,dt11)


def rebayer2x2RGGB(img,x,y) :

    rgb = rdd(img,x,y)

    return (rgb[0],rgb[1],rgb[1],rgb[2])

def rebayer2x2RGGBdel(img,x,y) :

    rgb = rdd(img,x+0,y+0)

    if x%2==0 and y%2==0 :
        return (rgb[0])
    if x%2==0 and y%2==1 :
        return (rgb[1])
    if x%2==1 and y%2==0 :
        return (rgb[1])
    if x%2==1 and y%2==1 :
        return (rgb[2])

    return (0)

def rebayer2x2RGGBrev(img,x,y) :

    red = 0
    grn = 0
    blu = 0

    for dy in (0,1) :
        for dx in (0,1) :
            rgb = rdd(img,x//2*2+dx,y//2*2+dy)
            red = red + rgb[0]
            grn = grn + rgb[1]
            blu = blu + rgb[2]

    ct = 4

    if x%2==0 and y%2==0 :
        return (red//ct)
    if x%2==0 and y%2==1 :
        return (grn//ct)
    if x%2==1 and y%2==0 :
        return (grn//ct)
    if x%2==1 and y%2==1 :
        return (blu//ct)

    return (0)

def rebayer3x3RGGBrev(img,x,y) :

    red = 0
    grn = 0
    blu = 0

    for dy in (-1,0,1) :
        for dx in (-1,0,1) :
            rgb = rdd(img,x+dx,y+dy)
            red = red + rgb[0]
            grn = grn + rgb[1]
            blu = blu + rgb[2]

    ct = 9
    if x == 0 or x == img.size[0] - 1 :
        ct = ct - 3
    if y == 0 or y == img.size[1] - 1 :
        ct = ct - 3
    if ct < 4 :
        ct = 4

    if x%2==0 and y%2==0 :
        return (red//ct)
    if x%2==0 and y%2==1 :
        return (grn//ct)
    if x%2==1 and y%2==0 :
        return (grn//ct)
    if x%2==1 and y%2==1 :
        return (blu//ct)

    return (0)


print(f"*** REBAYER PROGRAM VERSION:{ver} ***")
print("\nSELECT COLOR FILE\n")
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

        if md != "RGB" and md != "RGBA" :
            print(f"{fnm} : not color file.")
            continue

        print("*** CONVERT MODE ***")
        print("1: RGGB 1x1 ")
        print("2: RGGB 2x2 ")
        print("3: RGGB 3x3 ")

        while True :
            try :
                md = int(input("MODE :"))
                if 1 <= md and md <= 3 :
                    break
            except ValueError :
                continue

#       RE OPEN AS A BINARY

        with open(fnm,'rb') as f :
            data = f.read()
            img_src = Image.open(BytesIO(data))

#       CONVERT DATA
        img_cv = Image.new('L',(wd,ht))

        for y in range(img_src.size[1]) :
            for x in range(img_src.size[0]) :

                if md == 1:
                    bb  = rebayer2x2RGGBdel(img_src,x,y)
                    img_cv.putpixel((x+0,y+0),bb)

                if md == 2:
                    bb  = rebayer2x2RGGBrev(img_src,x,y)
                    img_cv.putpixel((x+0,y+0),bb)

                if md == 3:
                    bb  = rebayer3x3RGGBrev(img_src,x,y)
                    img_cv.putpixel((x+0,y+0),bb)

        fno = fnm + ".rebayered-" + str(md) + ".png"
        print(f"WRITE OUT : {fno}")
        img_cv.save(fno)

        print("*** DONE ***")

# EBD OF FILE
