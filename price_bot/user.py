import database as db
import sys
sys.path.insert(0, './../')
from item import Item

class User:

    def __init__(self, user_id, name=''):
        self.id = user_id
        self.user_name = name

        # Item objects

        self.item_list = []

    def add_item(self, url):
        item = Item(url)
        item.extract_info() # fetch soup and then name, price etc..
        db.ItemDb.get_or_create(owner=self.id,
                                name=item.name,
                                price=int(item.price),
                                url=item.url)
        self.item_list.append(item)

    def check_prices(self):
        updated_items = []

        for item in self.item_list:
            old_price = item.price
            item.update()

            if old_price != item.price:
                updated_items.append(item)

        notify_user(updated_items)

    def get_item_list(self):

        if len(self.item_list) == 0:
            self.get_items_from_database()

        result = []
        for i in range(len(self.item_list)):
            item = self.item_list[i]
            result.append(str(i+1) + "-) "
                          + item.name[:25]
                          + ": ₺" + str(int(item.price))
                          + "\n")

        if len(result) == 0:
            return "You have not added any item, type /add url"

        return "".join(result)

    def get_items_from_database(self):
        """ Get items from database and save in self.item_list
        """
        item_list = db.get_user_items(self.id)

        for item in item_list:
            custom_item = Item(item.url, item.name, item.price)
            self.item_list.append(custom_item)

        return self.item_list

