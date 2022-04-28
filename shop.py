# 趣味のPython学習　Project 01-03
# 雑貨屋パイソンちゃん
# ばーじょん 0.1.1

from shopitem import CommonItem 
from shopitem import FoodItem 
from shopitem import ToyItem 
from shopitem import FoodAndToyItem 

x1 = CommonItem(name="Spoon",price=200)
x1.show()

x2 = FoodItem(name="Bread",price=300,date="2022/05/10")
x2.show()

x3 = ToyItem(name="Minicar",price=500,age=6)
x3.show()

x4 = FoodAndToyItem(name="PrizeInFood",price=300,date="2022/07/10",age=5)
x4.show()
