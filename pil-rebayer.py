# 趣味のPython学習　Project 02-02
#
# COLOR-DATA TO BAYERD-DATA
# CONVERT PROGRAM
#   ( WITH PIL )
# ばーじょん 1.0.2

ver = "1.0.2"

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

def rebayer2x2RGGBmini(img,x,y) :

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


print(f"*** REBAYER PROGRAM ( with PIL ) VERSION:{ver}")
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
        print("1: GRAY     ( 2x image )")
        print("2: RGGB 2x2 ( 2x image )")
        print("3: RGGB 2x2 ( 1x image )")

        while True :
            md = int(input("MODE :"))
            if 1 <= md and md <= 3 :
                break

#       RE OPEN AS A BINARY

        with open(fnm,'rb') as f :
            data = f.read()
            img_src = Image.open(BytesIO(data))

        if md == 1 or md == 2 :
            wd = wd * 2
            ht = ht * 2

#       CONVERT DATA
        img_cv = Image.new('L',(wd,ht))

        for y in range(img_src.size[1]) :
            for x in range(img_src.size[0]) :
                if md == 1:
                    bb  = rebayer00RGGB(img_src,x,y)
                    img_cv.putpixel((x*2+0,y*2+0),bb[0])
                    img_cv.putpixel((x*2+1,y*2+0),bb[1])
                    img_cv.putpixel((x*2+0,y*2+1),bb[2])
                    img_cv.putpixel((x*2+1,y*2+1),bb[3])
                if md == 2:
                    bb  = rebayer2x2RGGB(img_src,x,y)
                    img_cv.putpixel((x*2+0,y*2+0),bb[0])
                    img_cv.putpixel((x*2+1,y*2+0),bb[1])
                    img_cv.putpixel((x*2+0,y*2+1),bb[2])
                    img_cv.putpixel((x*2+1,y*2+1),bb[3])
                if md == 3:
                    bb  = rebayer2x2RGGBmini(img_src,x,y)
                    img_cv.putpixel((x+0,y+0),bb)

        fno = fnm + ".rebayered-" + str(md) + ".png"
        print(f"WRITE OUT : {fno}")
        img_cv.save(fno)

        print("*** DONE ***")


