# 趣味のPython学習　Project 02-03
# Python PNG16 DEBAYER
# ばーじょん 1.0.5

ver = "1.0.5"

import zlib

from PIL import Image

# NEED THIS ! get with pip command !
import imageio

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

#       MIN-MAX CORRECT
        if val > maxval :
                val = maxval
        val = val - minval
        if val < 0 :
                val = 0

        if gnmval > 0.0 and gnmval != 1.0 :
                val = int((maxval-minval)*(float(val)/(maxval-minval))**(1/gnmval))

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

def shift_max(data) :

        buffer = []
        pw = max(data)
        dpos = 0

        for sf in range(0,8) :
                if pw<256 :
                        break
                pw = pw >> 1

        for i in range(len(data)//4) :
                alp = data[dpos]
                dpos = dpos + 1
                red = data[dpos]>>sf
                dpos = dpos + 1
                grn = data[dpos]>>sf
                dpos = dpos + 1
                blu = data[dpos]>>sf
                dpos = dpos + 1
                buffer.append((red,grn,blu,alp))

        return buffer

def div_max(data) :

        buffer = []
        pw = max(data)
        if pw<255 :
                pw = 255
        dpos = 0

        for i in range(len(data)//4) :
                alp = data[dpos]
                dpos = dpos + 1
                red = int(float(data[dpos])/pw*0x00FF)
                dpos = dpos + 1
                grn = int(float(data[dpos])/pw*0x00FF)
                dpos = dpos + 1
                blu = int(float(data[dpos])/pw*0x00FF)
                dpos = dpos + 1
                buffer.append((red,grn,blu,alp))

        return buffer

def cut_max(data) :

        buffer = []
        dpos = 0

        for i in range(len(data)//4) :
                alp = data[dpos]
                dpos = dpos + 1
                red = min([data[dpos],0x00FF])
                dpos = dpos + 1
                grn = min([data[dpos],0x00FF])
                dpos = dpos + 1
                blu = min([data[dpos],0x00FF])
                dpos = dpos + 1
                buffer.append((red,grn,blu,alp))

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

# CRC CHECK

def calc_crc0(crc, d, magic) :

        for i in range(8) :
                if ((d >> i) & 1) :
                        crc = crc ^ 1
                b = (crc & 1)
                crc = crc >> 1
                if b :
                        crc = crc ^ magic

        return crc

def crc_calc(crc, buff, magic) :

        for n in range(len(buff)) :
                crc = calc_crc0(crc,buff[n],magic)
        return crc


def change_val(st,val) :

        keyin = input(f"{st} : {val} = ")
        if len(keyin) == 0 :
                keyin = str(val)
        return keyin

# MAIN

print(f"*** PNG16-GRAY to TRUE-COLOR CONVERTER VERSION {ver} ***")
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

                        global minval
                        global maxval
                        global gnmval

                        minval = 0
                        maxval = 0xFFFF
                        gnmval = 1.0000

                        print("*** CORRECTION SETTING ***")

                        while True :
                                minval = int(  change_val("MIN",minval))
                                maxval = int(  change_val("MAX",maxval))
                                gnmval = float(change_val("GNM",gnmval))
                                if minval >= maxval :
                                        continue
                                if gnmval <= 0.0  :
                                        continue
                                break

                        print("*** CONVERT MODE ***")
                        print("1: SHIFT MAX")
                        print("2: DIV   MAX")
                        print("3: CUT   MAX")

                        mode = 0

                        while True :
                                mode = int(input("MODE :"))
                                if 1 <= mode and mode <= 3 :
                                        break

                        imagebuffer = imageio.v2.imread(fnm)

                        print("*** CONVERT FILE ***")

                        if dm == 1 :
                                imagebuffer = conv16to64RGGBGRY(imagebuffer,width,height)
                        if dm == 2 :
                                imagebuffer = conv16to64RGGB2x2(imagebuffer,width,height)
                        if dm == 3 :
                                imagebuffer = conv16to64RGGB3x3(imagebuffer,width,height)

                        if mode == 1 :
                                imagebuffer = shift_max(imagebuffer)
                        if mode == 2 :
                                imagebuffer = div_max(imagebuffer)
                        if mode == 3 :
                                imagebuffer = cut_max(imagebuffer)

                        img_cv = Image.new('RGBA',(width,height))

                        for y in range(height) :
                                for x in range(width) :
                                        img_cv.putpixel((x,y),imagebuffer[width*y+x])


                        fno = fnm + ".debayer-" + str(dm) + str(mode) + ".png"
                        print(f"*** WRITE OUT : {fno} ***")
                        img_cv.save(fno)

                        print("DONE !")
