import pygwidgets

class DisplayMoney(pygwidgets.DisplayText):
    def __init__(self, window, loc, value='', fontName=None, fontSize=20, 
                 width=150, height=None, textColor="Black",
                 backgroundColor=None, justified='left', nickname=None,
                 symbol = '$', symbol_to_left = True, 
                 show_cents = True):
        
        self.symbol = symbol
        self.symbol_to_left = symbol_to_left
        self.show_cents = show_cents
        if value is None:
            value = 0
        
        super().__init__(window, loc, value, fontName, fontSize, width, 
                         height, textColor, backgroundColor,
                         justified, nickname)
        
    def setValue(self, money):
        if money == '':
            money = 0.0
        money = float(money)
        if self.show_cents:
            money = '{:,.2f}'.format(money)
        else:
            money = '{:,.0f}'.format(money)
            
        if self.symbol_to_left:
            text = self.symbol + money
        else:
            text = money + self.symbol

        super().setValue(text)