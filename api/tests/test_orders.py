from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..controllers import menu_items as menu_controller
from ..main import app
import pytest
from ..models import orders as model
from ..models import menu_items as menu_model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"

def test_create_menu_item(db_session):
    menu_item_data = {
        'item_name': 'Porterhouse Steak',
        'price': 124.99,
        'calories': 4000,
        'food_category': 'Main Course',
        'description': 'A 16oz steak with a side of mashed potatoes and a salad' #creating a test for menu item creation
    }

    # Built MenuItem object the same way the database should receive it
    menu_object = menu_model.MenuItem(**menu_item_data)

    # Call the create function
    created_item = menu_controller.create(db_session, menu_object)

    assert created_item is not None #make sure it returns something and not none
    assert created_item.item_name == 'Porterhouse Steak' #checks if item name stored correctly
    assert created_item.food_category == 'Main Course' #  checks if food category stored correctly