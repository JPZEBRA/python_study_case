# 趣味のPython学習　Project 01-03
# 雑貨屋パイソンちゃん
# ばーじょん 0.1.1

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
        self._tax = 0

    def _set_tax(self, ratio):
        self._tax = round(self._price_o * ratio / (1 + ratio),2)

    def show_i(self):
        print(self._name, self._price_i)

    def show_o(self):
        print(self._name, self._price_o)

    def show_tax(self):
        print(self._name, self._price_o, "(" + str(self._tax) + ")")

class CommonItem(Item):

    def __init__(self, **rest):
        super().__init__(**rest)
        super()._set_tax(Item._tax_a)

    def show(self):
        super().show_tax()

class FoodItem(Item):

    def __init__(self, date, **rest):
        super().__init__(**rest)
        self._date = date
        super()._set_tax(Item._tax_f)

    def show(self):
        super().show_tax()
        print("date : ",self._date)

class ToyItem(Item):

    def __init__(self, age, **rest):
        super().__init__(**rest)
        self._age = age
        super()._set_tax(Item._tax_a)

    def show(self):
        super().show_tax()
        print("age : ",self._age)

class FoodAndToyItem(FoodItem,ToyItem):

    def __init__(self,**rest):
        super().__init__(**rest)
        super()._set_tax(Item._tax_f)

    def show(self):
        super().show_tax()
        print("date : ",self._date)
        print("age : ",self._age)

# ----- CLASS END -----