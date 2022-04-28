# 趣味のPython学習　Project 01-03
# 雑貨屋パイソンちゃん
# ばーじょん 0.1.0

class Item:

    _mergin = 0.3
    _tax_a = 0.10
    _tax_f = 0.08

    def __init__(self, name, price):
        self._name = name
        self._price_i = price
        plus = round(price * Item._mergin)
        if plus < 1 : plus = 1
        self._price_o = price + plus

    def show_i(self):
        print(self._name, self._price_i)

    def show_o(self):
        print(self._name, self._price_o)

    def show_tax_a(self):
        tax = round(self._price_o * Item._tax_a / (1 + Item._tax_a),2)
        print(self._name, self._price_o, "(" + str(tax) + ")")

    def show_tax_f(self):
        tax = round(self._price_o * Item._tax_f / (1 + Item._tax_f),2)
        print(self._name, self._price_o, "(" + str(tax) + ")" )

class CommonItem(Item):

    def __init__(self, **rest):
        super().__init__(**rest)

    def show(self):
        super().show_tax_a()

class FoodItem(Item):

    def __init__(self, date, **rest):
        super().__init__(**rest)
        self._date = date

    def show(self):
        super().show_tax_f()
        print("date : ",self._date)

class ToyItem(Item):

    def __init__(self, age, **rest):
        super().__init__(**rest)
        self._age = age

    def show(self):
        super().show_tax_a()
        print("age : ",self._age)

class FoodAndToyItem(FoodItem,ToyItem):

    def show(self):
        super().show_tax_f()
        print("date : ",self._date)
        print("age : ",self._age)




#
# NOW TESTING !!!
#

x1 = CommonItem(name="Spoon",price=200)
x1.show()

x2 = FoodItem(name="Bread",price=300,date="2022/05/10")
x2.show()

x3 = ToyItem(name="Minicar",price=500,age=6)
x3.show()

x4 = FoodAndToyItem(name="PrizeInFood",price=300,date="2022/07/10",age=5)
x4.show()
