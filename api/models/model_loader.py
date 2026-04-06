from . import orders, order_details, recipes, sandwiches, resources, menu_item

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
<<<<<<< HEAD
    menu_items.Base.metadata.create_all(engine) #added menu_items table
=======
    menu_item.Base.metadata.create_all(engine)
>>>>>>> origin/main
