# 趣味のPython学習　Project 02-00
# Python PNG08-Debayer ( RGGB )
# FULL SCRATCH CODE
# ばーじょん 1.0.6

ver = "1.0.6"

import zlib

# DATA ACCESS

def rdd(data,x,y,w,h) :

        if x < 0 :
                return 0
        if y < 0 :
                return 0

        dt11 = data[ (w+1)*y + x + 1]

        return dt11

def rdb(data,x,y,w,h) :

        if x < 0 :
                return 0
        if y < 0 :
                return 0

        dt11 = data[ w*y + x ]

        return dt11

def rdf(data,x,y,c,w,h) :

        if x < 0 :
                return 0
        if y < 0 :
                return 0

        dt11 = data[ (w*3)*y + x*3 + c ]

        return dt11

def rdw(data,x,y,w,h) :

        if x < 0 :
                return 0
        if y < 0 :
                return 0

        dt11 = data[ (w*2)*y + x*2 + 0]
        dt12 = data[ (w*2)*y + x*2 + 1]

        return ( dt11<<8 | dt12 )

# DEBAYER

def rgb08C2x2(data,x,y,w,h) :

        xx = x // 2
        yy = y // 2 


        try :
                dt11 = rdb(data,xx*2+0,yy*2+0,w,h)
                dt12 = rdb(data,xx*2+1,yy*2+0,w,h)
                dt13 = rdb(data,xx*2+0,yy*2+1,w,h)
                dt14 = rdb(data,xx*2+1,yy*2+1,w,h)
 
                dt15 = ( dt12 + dt13 ) // 2

                return bytes([dt11,dt15,dt14])

        except IndexError:
                pass

        return bytes([0,0,0])

def rgb16C2x2(data,x,y,w,h) :

        xx = x // 2
        yy = y // 2 


        try :
                dt11 = rdw(data,xx*2+0,yy*2+0,w,h)
                dt12 = rdw(data,xx*2+1,yy*2+0,w,h)
                dt13 = rdw(data,xx*2+0,yy*2+1,w,h)
                dt14 = rdw(data,xx*2+1,yy*2+1,w,h)
 
                dt15 = ( dt12 + dt13 ) // 2

                return ([dt11,dt15,dt14])

        except IndexError:
                pass

        return ([0,0,0])

def rgb08C3x3(data,x,y,w,h) :

        try :
                dt11 = rdb(data, x-1 ,y-1, w,h)
                dt12 = rdb(data, x+0 ,y-1, w,h)
                dt13 = rdb(data, x+1 ,y-1, w,h)

                dt21 = rdb(data, x-1 ,y+0, w,h)
                dt22 = rdb(data, x+0 ,y+0, w,h)
                dt23 = rdb(data, x+1 ,y+0, w,h)

                dt31 = rdb(data, x-1 ,y+1, w,h)
                dt32 = rdb(data, x+0 ,y+1, w,h)
                dt33 = rdb(data, x+1 ,y+1, w,h)

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
        
                return bytes([red,grn,blu])

        except IndexError:
                pass

        return bytes([0,0,0])

def rgb16C3x3(data,x,y,w,h) :

        try :
                dt11 = rdw(data, x-1 ,y-1, w,h)
                dt12 = rdw(data, x+0 ,y-1, w,h)
                dt13 = rdw(data, x+1 ,y-1, w,h)

                dt21 = rdw(data, x-1 ,y+0, w,h)
                dt22 = rdw(data, x+0 ,y+0, w,h)
                dt23 = rdw(data, x+1 ,y+0, w,h)

                dt31 = rdw(data, x-1 ,y+1, w,h)
                dt32 = rdw(data, x+0 ,y+1, w,h)
                dt33 = rdw(data, x+1 ,y+1, w,h)

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
        
                return ([red,grn,blu])

        except IndexError:
                pass

        return ([0,0,0])

def rgb08M1x1(data,x,y,w,h) :

        dt11 = rdb(data,x,y,w,h)

        red = dt11
        grn = dt11
        blu = dt11

        return bytes([red,grn,blu])

def rgb16M1x1(data,x,y,w,h) :

        dt11 = rdw(data,x,y,w,h)

        red = dt11
        grn = dt11
        blu = dt11

        return ([red,grn,blu])


# LINE FILTER

def check_filter(data,x,y,w,h) :

        dt11 = data[(w+1)*y]
        return dt11

# Paeth Predictor

def fl_pp(a,b,c) :

        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)

        if pa <= pb and pa <= pc :
                return a
        if pb <= pc :
                return b
        return c

# DECODE

def defilter08(data,w,h,bfr) :

        buffer = bytearray(w*h*3)
        bpos = 0

        for i in range(0,h) :

                fl = check_filter (data,0,i,w,h)

                for j in range(0,w) :

                        dt11 = 0

                        if fl>=5 :
                                print("* FILTER ERROR  *") 
                        if fl==4 :
                                dt11 = ( rdd(data,j,i,w,h) + fl_pp( rdb(buffer,j-bfr,i,w,h), rdb(buffer,j,i-1,w,h), rdb(buffer,j-bfr,i-1,w,h) ) ) % 256
                        if fl==3 :
                                dt11 = ( rdd(data,j,i,w,h) + ( ( rdb(buffer,j-bfr,i,w,h) + rdb(buffer,j,i-1,w,h) )//2 ) ) % 256
                        if fl==2 :
                                dt11 = ( rdd(data,j,i,w,h) + rdb(buffer,j,i-1,w,h) ) % 256
                        if fl==1 :
                                dt11 = ( rdd(data,j,i,w,h) + rdb(buffer,j-bfr,i,w,h) ) % 256
                        if fl==0 :
                                dt11 = rdd(data,j,i,w,h)

                        buffer[bpos] = dt11
                        bpos = bpos + 1

        return buffer

# DEBAYER 08

def convert08(data,w,h,md,fl) :

        wd = w
        ht = h
        pd = 3

        buffer = bytearray(wd*ht*pd+ht)
        bpos = 0

#       DEBAYER

        for hgt in range(0,ht) :

                if hgt%100 == 0 :
                        print("LINE:",hgt)

                for wdh in range(0,wd) :

                        if md == 1 or md <1 :
                                bb = rgb08M1x1(data,wdh,hgt,w,h)
                        if md == 2 :
                                bb = rgb08C2x2(data,wdh,hgt,w,h)
                        if md == 3 or md > 3 :
                                bb = rgb08C3x3(data,wdh,hgt,w,h)

                        buffer[bpos + 0] = bb[0]
                        buffer[bpos + 1] = bb[1]
                        buffer[bpos + 2] = bb[2]
                        bpos = bpos + pd

        return setfilter08(buffer,w,h,fl)

# FILTER 08

def setfilter08(buffer,w,h,fl) :

        wd = w
        ht = h
        pd = 3

        filterd = bytearray(wd*ht*pd+ht)
        bpos = 0

        for hgt in range(0,ht) :

                filterd[bpos] = fl
                bpos = bpos + 1

                if hgt%100 == 0 :
                        print("LINE:",hgt)

                for wdh in range(0,wd) :

                        if fl == 0:
                               b0 = rdf(buffer,wdh,hgt,0,w,h)
                               b1 = rdf(buffer,wdh,hgt,1,w,h)
                               b2 = rdf(buffer,wdh,hgt,2,w,h)
                        if fl == 1:
                               b0 = ( rdf(buffer,wdh,hgt,0,w,h) - rdf(buffer,wdh-1,hgt,0,w,h) ) % 256
                               b1 = ( rdf(buffer,wdh,hgt,1,w,h) - rdf(buffer,wdh-1,hgt,1,w,h) ) % 256
                               b2 = ( rdf(buffer,wdh,hgt,2,w,h) - rdf(buffer,wdh-1,hgt,2,w,h) ) % 256
                        if fl == 2:
                               b0 = ( rdf(buffer,wdh,hgt,0,w,h) - rdf(buffer,wdh,hgt-1,0,w,h) ) % 256
                               b1 = ( rdf(buffer,wdh,hgt,1,w,h) - rdf(buffer,wdh,hgt-1,1,w,h) ) % 256
                               b2 = ( rdf(buffer,wdh,hgt,2,w,h) - rdf(buffer,wdh,hgt-1,2,w,h) ) % 256
                        if fl == 3:
                               b0 = ( rdf(buffer,wdh,hgt,0,w,h) - ( ( rdf(buffer,wdh-1,hgt,0,w,h) + rdf(buffer,wdh,hgt-1,0,w,h) )//2 ) ) % 256
                               b1 = ( rdf(buffer,wdh,hgt,1,w,h) - ( ( rdf(buffer,wdh-1,hgt,1,w,h) + rdf(buffer,wdh,hgt-1,1,w,h) )//2 ) ) % 256
                               b2 = ( rdf(buffer,wdh,hgt,2,w,h) - ( ( rdf(buffer,wdh-1,hgt,2,w,h) + rdf(buffer,wdh,hgt-1,2,w,h) )//2 ) ) % 256

                        filterd[bpos + 0] = b0
                        filterd[bpos + 1] = b1
                        filterd[bpos + 2] = b2
                        bpos = bpos + pd

        return filterd

# DEBAYER 16

def convert16(data,w,h,md,fl) :

        wd = w
        ht = h

        wbf = []

#       DEBAYER

        for hgt in range(0,ht) :

                if hgt%100 == 0 :
                        print("LINE:",hgt)

                for wdh in range(0,wd) :

                        if md == 1 or md <1 :
                                ww = rgb16M1x1(data,wdh,hgt,w,h)
                        if md == 2 :
                                ww = rgb16C2x2(data,wdh,hgt,w,h)
                        if md == 3 or md > 3 :
                                ww = rgb16C3x3(data,wdh,hgt,w,h)

                        wbf.append(ww[0])
                        wbf.append(ww[1])
                        wbf.append(ww[2])
 
        return setfilter08(tobytes(correct(wbf)),w,h,fl)

# VALUE CORRECTION

def change_val(st,val) :

        keyin = input(f"{st} : {val} = ")
        if len(keyin) == 0 :
                keyin = str(val)
        return keyin

def correct(wbf) :

        lg   = len(wbf)

        rmin = 0xFFFF
        rmax = 0x0000
        gmin = 0xFFFF
        gmax = 0x0000
        bmin = 0xFFFF
        bmax = 0x0000

        pos = 0

        while pos < lg :
                if wbf[pos] < rmin : rmin = wbf[pos]
                if wbf[pos] > rmax : rmax = wbf[pos]
                pos = pos + 1
                if wbf[pos] < gmin : gmin = wbf[pos]
                if wbf[pos] > gmax : gmax = wbf[pos]
                pos = pos + 1
                if wbf[pos] < bmin : bmin = wbf[pos]
                if wbf[pos] > bmax : bmax = wbf[pos]
                pos = pos + 1
        print(f"RED {rmin}-{rmax} GRN {gmin}-{gmax} BLU {bmin}-{bmax} ")

        minval = 0x0000
        maxval = 0xFFFF
        gnmval = 1.0000

        while True :
                try :
                        minval = int  (change_val("MIN",minval))
                        maxval = int  (change_val("MAX",maxval))
                        gnmval = float(change_val("GNM",gnmval))
                except ValueError :
                        continue
                if minval >= maxval :
                        continue
                if gnmval <= 0 :
                        continue
                break

        dbf = []

        for n in range(0,lg) :

                val = wbf[n]

#               MIN-MAX CORRECT
                if val > maxval :
                        val = maxval
                        val = val - minval
                if val < 0 :
                        val = 0
#               GANMMA CORRECT
                if gnmval > 0.0 and gnmval != 1.0 :
                        val = int((maxval-minval)*(float(val)/(maxval-minval))**(1/gnmval))

                dbf.append(val)

        return dbf

# SET TO BYTE

def tobytes(wbf) :

        buffer = []

        lg = len(wbf)
        mx = max(wbf)
        sf = 0

        if mx < 256 :
                mode = 3
        else :

                print(f"MAX VALUE : {mx} ")
                print("1: SFT MAX")
                print("2: DIV MAX")
                print("3: CUT MAX")

                while True :
                        try :
                                mode = int(input("MODE : "))
                        except ValueError :
                                continue
                        if 1 <= mode and mode <= 3 :
                                break
 
        if mode == 1 :
                for n in range(0,8) :
                        if mx < 256 :
                                break
                        mx = mx >> 1
                        sf = sf + 1
                for n in range(0,lg) :
                        buffer.append(wbf[n]>>sf)
        if mode == 2 :
                for n in range(0,lg) :
                        buffer.append(wbf[n]*255//mx)
        if mode == 3 :
                for n in range(0,lg) :
                        buffer.append(min([wbf[n],0x00FF]))

        return buffer


# DATA CONVERT

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

# CRC CHECKER

magic = 0xEDB88320

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

# WRITE OUT PNG

def writefile(fname,width,height,data) :

        wd = width
        ht = height

        f = open(fname,'wb')
        f.write(b'\x89' )
        f.write(b'PNG' )
        f.write(b'\x0d\x0a' )
        f.write(b'\x1a\x0a' )

        f.write(bytes4(13))

        f.write(b'IHDR' )
        f.write(bytes4(wd))
        f.write(bytes4(ht))
        f.write(bytes1(8))
        f.write(bytes1(2))
        f.write(bytes1(0))
        f.write(bytes1(0))
        f.write(bytes1(0))

        crc   = 0xFFFFFFFF
        crc = crc_calc(crc,b'IHDR',magic)
        crc = crc_calc(crc,bytes4(wd),magic)
        crc = crc_calc(crc,bytes4(ht),magic)
        crc = crc_calc(crc,bytes1(8),magic)
        crc = crc_calc(crc,bytes1(2),magic)
        crc = crc_calc(crc,bytes1(0),magic)
        crc = crc_calc(crc,bytes1(0),magic)
        crc = crc_calc(crc,bytes1(0),magic)
        crc   = 0xFFFFFFFF - crc
        f.write(bytes4(crc))

        bsz = 8184
        idx = 0
        dlen = len(data)

        while idx + bsz <= dlen :

                f.write(bytes4(bsz))
                f.write(b'IDAT' )
                f.write(data[idx:idx+bsz])

                crc   = 0xFFFFFFFF
                crc = crc_calc(crc,b'IDAT',magic)
                crc = crc_calc(crc,data[idx:idx+bsz],magic)
                crc   = 0xFFFFFFFF - crc
                f.write(bytes4(crc))

                idx = idx + bsz

        if idx<dlen :

                f.write(bytes4(dlen-idx))
                f.write(b'IDAT' )
                f.write(data[idx:])

                crc   = 0xFFFFFFFF
                crc = crc_calc(crc,b'IDAT',magic)
                crc = crc_calc(crc,data[idx:],magic)
                crc   = 0xFFFFFFFF - crc
                f.write(bytes4(crc))

        f.write(bytes4(0))
        f.write(b'IEND' )

        crc   = 0xFFFFFFFF
        crc = crc_calc(crc,b'IEND',magic)
        crc   = 0xFFFFFFFF - crc
        f.write(bytes4(crc))

        f.close()

# MAIN

print(f"*** PNG08 DEBAYER PROGRAM ( FULL SCRATCH ) VERSION {ver} ***")
print("SELECT PNG08 GRAY SCALE FILE : ")

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
                        if bit != 8 and bit != 16 :
                                print("BIT SIZE ERROR !")
                                assert(False)

                except AssertionError:
                        print("DATA ERROR !")
                        f.close()

                else :

                        try :

                                ipos = 0

                                safety = 5000

                                if bit ==  8 :
                                        imagebuffer = bytearray(width*height+safety)
                                if bit == 16 :
                                        imagebuffer = bytearray(width*2*height+safety)

                                while True :

                                        db = f.read(4)
                                        sb = f.read(4)

                                        size  = (((db[0]*256 + db[1])*256 + db[2])*256 + db[3])

                                        if sb == b'IDAT' :

                                                buffer = f.read(size)
                                                crc = f.read(4)

                                                for i in range(size) :
                                                        imagebuffer[ipos] = buffer[i]
                                                        ipos = ipos + 1

                                                continue


                                        if sb == b'IEND' :
                                                assert(size == 0 )
                                                crc = f.read(4)
                                                f.close()
                                                break

                                        buffer = f.read(size)
                                        crc = f.read(4)

                                rawdata = zlib.decompress(imagebuffer)

                                print("BUFFER:",len(rawdata))

                                print("*** DEBAYER MODE ***")
                                print("1: GRAY")
                                print("2: RGGB 2x2")
                                print("3: RGGB 3x3")

                                while True :
                                        try :
                                                md = int(input("MODE :"))
                                                if 1 <= md and md <= 3 :
                                                        break
                                        except ValueError :
                                                continue

                                print("*** FILTER MODE ***")
                                print("0: NON")
                                print("1: SUB")
                                print("2: U P")
                                print("3: ABE")
                                print("4: PAE")


                                while True :
                                        try :
                                                fl = int(input("FILTER :"))
                                                if 0 <= fl and fl <= 3 :
                                                        break
                                        except ValueError :
                                                continue

                                print("*** CONVERT FILE ***")

                                if bit ==  8 :
                                        cbuffer = convert08(defilter08(rawdata,width,height,1),width,height,md,fl)
                                if bit == 16 :
                                        cbuffer = convert16(defilter08(rawdata,width*2,height,2),width,height,md,fl)

                                buffer = zlib.compress(cbuffer)

                                print("RGB:",len(buffer))

                                fno = fnm + ".dev" + str(md) + ".png"


                                print(f"*** WRITE OUT {fno} ***")

                                writefile(fno,width,height,buffer)

                                print("*** DONE ***")

                        except AssertionError:
                                print("DATA ERROR !")
                                f.close()
                        except IndexError:
                                print("BUFFER ERROR !")
                                f.close()
                        else :
                                pass

# END OF FILE