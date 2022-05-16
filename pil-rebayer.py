# 趣味のPython学習　Project 02-02
#
# COLOR-DATA TO BAYERD-DATA
# CONVERT PROGRAM
#   ( WITH PIL )
# ばーじょん 1.0.1

ver = "1.0.1"

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

def rebayer2x2RGGB(img,x,y) :

    rgb = rdd(img,x,y)

    return (rgb[0],rgb[1],rgb[1],rgb[2])

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

        md = 2

#       RE OPEN AS A BINARY

        with open(fnm,'rb') as f :
            data = f.read()
            img_src = Image.open(BytesIO(data))

#       CONVERT DATA
        img_cv = Image.new('L',(img_src.size[0]*2,img_src.size[1]*2))

        for y in range(img_src.size[1]) :
            for x in range(img_src.size[0]) :
                bb  = rebayer2x2RGGB(img_src,x,y)
                img_cv.putpixel((x*2+0,y*2+0),bb[0])
                img_cv.putpixel((x*2+1,y*2+0),bb[1])
                img_cv.putpixel((x*2+0,y*2+1),bb[2])
                img_cv.putpixel((x*2+1,y*2+1),bb[3])

        fno = fnm + ".rebayered-" + str(md) + ".png"
        print(f"WRITE OUT : {fno}")
        img_cv.save(fno)

        print("*** DONE ***")


