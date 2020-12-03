class Menu():
    def __init__(self, name, **kwargs):
        self.name = name
        ## can add more attributes from **kwargs like currency, price, etc

    def __str__(self):
        return self.name

class Restaurant():
    def __init__(self, id, name, city, **kwargs):
        self.id = id
        self.name = name
        self.city = city
        self.menus = {}
        ## can add more attributes from **kwargs like address, category, etc

    def addMenu(self, menuObj):
        self.menus[menuObj.name] = menuObj

    def toDict(self):
        dic = {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'menus': [menu.name for menu in self.menus.values()]
        }
        return dic
