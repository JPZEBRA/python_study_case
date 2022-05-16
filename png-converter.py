# 趣味のPython学習　Project 02-03
# Python PNG-Converter
# ばーじょん 1.0.1

ver = "1.0.1"

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

        return data[y][x]

def conv16to64(data,w,h) :

        buffer = []

        for y in range(0,h) :

                for x in range(0,w) :

                        red = rdd(data,(x>>1)*2 + 0,(y>>1)*2 + 0,w,h)
                        gr1 = rdd(data,(x>>1)*2 + 1,(y>>1)*2 + 0,w,h)
                        gr2 = rdd(data,(x>>1)*2 + 0,(y>>1)*2 + 1,w,h)
                        blu = rdd(data,(x>>1)*2 + 1,(y>>1)*2 + 1,w,h)

                        grn = (( 0xFFFF & gr1 ) + gr2) // 2
                        alp = 0xFF

                        buffer.append(alp)
                        buffer.append(red)
                        buffer.append(grn)
                        buffer.append(blu)

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
                red = int(float(data[dpos])/pw*0xFF)
                dpos = dpos + 1
                grn = int(float(data[dpos])/pw*0xFF)
                dpos = dpos + 1
                blu = int(float(data[dpos])/pw*0xFF)
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


# MAIN

print(f"*** PNG16 to TRUE-COLOR CONVERTER VERSION {ver}***")

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

                        print("*** CONVERT MODE ***")
                        print("1: SHIFT MAX")
                        print("2: DIV   MAX")

                        mode = 0

                        while True :
                                mode = int(input("MODE :"))
                                if 1 <= mode and mode <= 2 :
                                        break

                        imagebuffer = imageio.v2.imread(fnm)

                        print("*** CONVERT FILE ***")

                        imagebuffer = conv16to64(imagebuffer,width,height)

                        if mode == 1 :
                                imagebuffer = shift_max(imagebuffer)
                        if mode == 2 :
                                imagebuffer = div_max(imagebuffer)

                        img_cv = Image.new('RGBA',(width,height))

                        for y in range(height) :
                                for x in range(width) :
                                        img_cv.putpixel((x,y),imagebuffer[width*y+x])


                        fno = fnm + ".debayer-" + str(mode) + ".png"
                        print(f"*** WRITE OUT : {fno} ***")
                        img_cv.save(fno)

                        print("DONE !")