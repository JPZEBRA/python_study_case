# 趣味のPython学習　Project 01-03
# 雑貨屋パイソンちゃん
# ばーじょん 0.1.2

from shopitem import CommonItem 
from shopitem import FoodItem 
from shopitem import ToyItem 
from shopitem import FoodAndToyItem 

itemlist = []

# 仕入れ

while len( nm := input("Item : ") ) > 0 :
        try :
                while ( pr := int(input("Price : "))) <= 0 : pass
                dt = input("Date to use : ")
                while ( len( ag := input("Age : "))) > 0:
                        if int(ag)>0 : break
        except ValueError:
                pass
        else :
                if len(dt) == 0 and len(ag) == 0 :
                        itemlist.append(CommonItem(name=nm,price=pr))
                if len(dt) > 0 and len(ag) == 0 :
                        itemlist.append(FoodItem(name=nm,price=pr,date=dt))
                if len(dt) == 0 and len(ag) > 0 :
                        itemlist.append(ToyItem(name=nm,price=pr,age=ag))
                if len(dt) > 0 and len(ag) > 0 :
                        itemlist.append(FoodAndToyItem(name=nm,price=pr,date=dt,age=ag))

# 在庫確認

for item in itemlist :
        print("********************")
        item.show()

input("HIT ANY KEY")