# 趣味のPython学習　Project 02-04
# Python PNG16 CONVERTER
# ばーじょん 1.0.1

ver = "1.0.1"

from PIL import Image

# NEED THIS ! get 'imageio' with pip command !
import imageio

# NEED THIS ! get 'opencv-python' with pip command !
import cv2

import numpy as np

# DATA ACCESS

def rdd(data,x,y,w,h) :

        if x < 0 :
                return 0
        if y < 0 :
                return 0
        if x >= w :
                return 0
        if y >= h :
                return 0

        val = data[y][x]

        return val

def conv16to64RGGBGRY(data,w,h) :

        buffer = []

        for y in range(0,h) :

                for x in range(0,w) :

                        gry = rdd(data,x,y,w,h)

                        alp = 0xFF

                        buffer.append(alp)
                        buffer.append(gry)
                        buffer.append(gry)
                        buffer.append(gry)

        return buffer

def conv16to64RGGB2x2(data,w,h) :

        buffer = []

        for y in range(0,h) :

                for x in range(0,w) :

                        red = rdd(data,(x>>1)*2 + 0,(y>>1)*2 + 0,w,h)
                        gr1 = rdd(data,(x>>1)*2 + 1,(y>>1)*2 + 0,w,h)
                        gr2 = rdd(data,(x>>1)*2 + 0,(y>>1)*2 + 1,w,h)
                        blu = rdd(data,(x>>1)*2 + 1,(y>>1)*2 + 1,w,h)

#                       avoid over flow
                        grn = (( 0x0000FFFF & gr1 ) + gr2) // 2
                        alp = 0xFF

                        buffer.append(alp)
                        buffer.append(red)
                        buffer.append(grn)
                        buffer.append(blu)

        return buffer

def RGGB3x3(data,x,y,w,h) :


        dt11 = rdd(data,x-1,y-1,w,h)
        dt12 = rdd(data,x+0,y-1,w,h)
        dt13 = rdd(data,x+1,y-1,w,h)

        dt21 = rdd(data,x-1,y+0,w,h)
        dt22 = rdd(data,x+0,y+0,w,h)
        dt23 = rdd(data,x+1,y+0,w,h)

        dt31 = rdd(data,x-1,y+1,w,h)
        dt32 = rdd(data,x+0,y+1,w,h)
        dt33 = rdd(data,x+1,y+1,w,h)

        alp = 0xFF

        if x%2==0 and y%2==0 :
                red = dt22
                grn = ((0x0000FFFF & dt12 ) + dt21 + dt23 + dt32)//4
                blu = ((0x0000FFFF & dt11 ) + dt13 + dt31 + dt33)//4
        if x%2==0 and y%2==1 :
                red = ((0x0000FFFF & dt12 ) + dt32)//2
                grn = dt22
                blu = ((0x0000FFFF & dt21 ) + dt23)//2
        if x%2==1 and y%2==0 :
                red = ((0x0000FFFF & dt21 ) + dt23)//2
                grn = dt22
                blu = ((0x0000FFFF & dt12 ) + dt32)//2
        if x%2==1 and y%2==1 :
                red = ((0x0000FFFF & dt11 ) + dt13 + dt31 + dt33)//4
                blu = dt22
                grn = ((0x0000FFFF & dt12 ) + dt21 + dt23 + dt32)//4

        return (alp,red,grn,blu)

def conv16to64RGGB3x3(data,w,h) :

        buffer = []

        for y in range(0,h) :
                for x in range(0,w) :
                        RGBA = RGGB3x3(data,x,y,w,h)
                        buffer.append(RGBA[0])
                        buffer.append(RGBA[1])
                        buffer.append(RGBA[2])
                        buffer.append(RGBA[3])

        return buffer

# VALUE CONVERT

def value4(lb) :
        return (((lb[0]*256 + lb[1])*256 + lb[2])*256 + lb[3])

def bytes4(val) :
        b0 = val % 256
        val = val // 256
        b1 = val % 256
        val = val // 256
        b2 = val % 256
        val = val // 256
        b3 = val
        return bytes([b3,b2,b1,b0])

def bytes1(val) :
        return bytes([val])

magic = 0xEDB88320

# MAIN

print(f"*** PNG16-GRAY to TIFF CONVERTER VERSION {ver} ***")
print("\nSELECT PNG16 GRAY SCALE FILE\n")

while len( fnm := input("file : ") ) > 0 :

        try :
                f = open(fnm,'rb')
                assert(f.read(1)== b'\x89' )
                assert(f.read(3)== b'PNG' )
                assert(f.read(2)== b'\x0d\x0a')
                assert(f.read(2)== b'\x1a\x0a')
                print("PNG FORMAT ACCEPTED...")

        except FileNotFoundError:
                print("FILE NOT FOUND !")
        except AssertionError:
                print("TYPE ERROR !")
                f.close()
        else :
                try :
                        lb = f.read(4)
                        ln  = value4(lb)

                        assert(ln == 13)
                        assert(f.read(4) == b'IHDR')
                        wb = f.read(4)
                        hb = f.read(4)
                        bb = f.read(1)
                        cb = f.read(1)

                        pb = f.read(1)

                        yet = f.read(2)

                        crc = f.read(4)

                        width  = (((wb[0]*256 + wb[1])*256 + wb[2])*256 + wb[3])
                        height = (((hb[0]*256 + hb[1])*256 + hb[2])*256 + hb[3])
                        bit = bb[0]*1
                        col = cb[0]*1

                        cmp = pb[0]*1

                        print("W:",width,"H:",height)
                        print("B:",bit,"C:",col,"P:",cmp)

                        if col>0 :
                                print("NOT GRAY SCALE !")
                                assert(False)
                        if bit != 16 :
                                print("BIT SIZE ERROR !")
                                assert(False)
                except AssertionError:
                        print("DATA ERROR !")
                        f.close()
                        continue
                else :
                        f.close()

                        print("*** DEBAYER MODE ***")
                        print("1: GRAY")
                        print("2: RGGB 2x2")
                        print("3: RGGB 3x3")

                        while True :
                                dm = int(input("MODE :"))
                                if 1 <= dm and dm <= 3 :
                                        break


                        imagebuffer = imageio.v2.imread(fnm)

                        print("*** CONVERT FILE ***")

                        if dm == 1 :
                                imagebuffer = conv16to64RGGBGRY(imagebuffer,width,height)
                        if dm == 2 :
                                imagebuffer = conv16to64RGGB2x2(imagebuffer,width,height)
                        if dm == 3 :
                                imagebuffer = conv16to64RGGB3x3(imagebuffer,width,height)

                        img_cv = np.zeros((height,width,3),dtype=np.uint16)


                        for y in range(height) :
                                for x in range(width) :
                                        img_cv[y,x,0] = imagebuffer[width*4*y+x*4+3]
                                        img_cv[y,x,1] = imagebuffer[width*4*y+x*4+2]
                                        img_cv[y,x,2] = imagebuffer[width*4*y+x*4+1]


                        fno = fnm + ".debayer-" + str(dm) + ".tiff"
                        print(f"*** WRITE OUT : {fno} ***")
                        cv2.imwrite(fno,img_cv)

                        print("DONE !")
