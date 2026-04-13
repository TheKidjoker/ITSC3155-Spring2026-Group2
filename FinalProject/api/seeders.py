from datetime import datetime, timedelta
from .dependencies.database import SessionLocal
from .models.resources import Resource
from .models.sandwiches import Sandwich
from .models.recipes import Recipe
from .models.menu_items import MenuItem
from .models.promotions import Promotion
from .models.orders import Order
from .models.order_details import OrderDetail
from .models.payments import Payment
from .models.reviews import Review


def seed_data():
    print("[SEEDER] Starting seed_data...")
    db = SessionLocal()
    try:
        # Check if data already exists — if sandwiches are present, skip seeding
        if db.query(Sandwich).first() is not None:
            print("[SEEDER] Data already exists, skipping.")
            return

        # 1. Resources (ingredients)
        resources = [
            Resource(item="Bread", amount=100),
            Resource(item="Lettuce", amount=80),
            Resource(item="Tomato", amount=60),
            Resource(item="Turkey", amount=50),
            Resource(item="Cheese", amount=70),
            Resource(item="Bacon", amount=40),
        ]
        db.add_all(resources)
        db.flush()

        # 2. Sandwiches
        sandwiches = [
            Sandwich(sandwich_name="BLT", price=6.99),
            Sandwich(sandwich_name="Turkey Club", price=8.49),
            Sandwich(sandwich_name="Grilled Cheese", price=5.49),
            Sandwich(sandwich_name="Veggie", price=5.99),
        ]
        db.add_all(sandwiches)
        db.flush()

        # Build lookup dicts for FK references
        res_map = {r.item: r.id for r in resources}
        sand_map = {s.sandwich_name: s.id for s in sandwiches}

        # 3. Recipes (link ingredients to sandwiches)
        recipes = [
            # BLT
            Recipe(sandwich_id=sand_map["BLT"], resource_id=res_map["Bread"], amount=2),
            Recipe(sandwich_id=sand_map["BLT"], resource_id=res_map["Bacon"], amount=4),
            Recipe(sandwich_id=sand_map["BLT"], resource_id=res_map["Lettuce"], amount=1),
            Recipe(sandwich_id=sand_map["BLT"], resource_id=res_map["Tomato"], amount=2),
            # Turkey Club
            Recipe(sandwich_id=sand_map["Turkey Club"], resource_id=res_map["Bread"], amount=3),
            Recipe(sandwich_id=sand_map["Turkey Club"], resource_id=res_map["Turkey"], amount=3),
            Recipe(sandwich_id=sand_map["Turkey Club"], resource_id=res_map["Cheese"], amount=1),
            Recipe(sandwich_id=sand_map["Turkey Club"], resource_id=res_map["Lettuce"], amount=1),
            Recipe(sandwich_id=sand_map["Turkey Club"], resource_id=res_map["Tomato"], amount=1),
            Recipe(sandwich_id=sand_map["Turkey Club"], resource_id=res_map["Bacon"], amount=2),
            # Grilled Cheese
            Recipe(sandwich_id=sand_map["Grilled Cheese"], resource_id=res_map["Bread"], amount=2),
            Recipe(sandwich_id=sand_map["Grilled Cheese"], resource_id=res_map["Cheese"], amount=3),
            # Veggie
            Recipe(sandwich_id=sand_map["Veggie"], resource_id=res_map["Bread"], amount=2),
            Recipe(sandwich_id=sand_map["Veggie"], resource_id=res_map["Lettuce"], amount=2),
            Recipe(sandwich_id=sand_map["Veggie"], resource_id=res_map["Tomato"], amount=3),
            Recipe(sandwich_id=sand_map["Veggie"], resource_id=res_map["Cheese"], amount=1),
        ]
        db.add_all(recipes)
        db.flush()

        # 4. Menu Items (the 4 sandwiches + a drink/side)
        menu_items = [
            MenuItem(item_name="BLT", price=6.99, calories=450, food_category="Sandwich", description="Classic bacon, lettuce, and tomato"),
            MenuItem(item_name="Turkey Club", price=8.49, calories=520, food_category="Sandwich", description="Triple-decker turkey club"),
            MenuItem(item_name="Grilled Cheese", price=5.49, calories=380, food_category="Sandwich", description="Melted cheese on toasted bread"),
            MenuItem(item_name="Veggie", price=5.99, calories=300, food_category="Sandwich", description="Fresh veggies on whole wheat"),
            MenuItem(item_name="Fountain Drink", price=1.99, calories=150, food_category="Beverage", description="Choice of soda"),
        ]
        db.add_all(menu_items)
        db.flush()

        menu_map = {m.item_name: m.id for m in menu_items}

        # 5. Promotions
        promotions = [
            Promotion(code="WELCOME10", discount_percentage=10.00, expiration_date=datetime.now() + timedelta(days=90), is_active=True),
            Promotion(code="SUMMER20", discount_percentage=20.00, expiration_date=datetime.now() + timedelta(days=60), is_active=True),
            Promotion(code="SAVE5", discount_amount=5.00, expiration_date=datetime.now() + timedelta(days=30), is_active=True),
        ]
        db.add_all(promotions)
        db.flush()

        promo_map = {p.code: p.id for p in promotions}

        # 6. Orders (different statuses, some with promotions)
        orders = [
            Order(
                customer_name="Alice Johnson",
                email="alice@example.com",
                phone="704-555-0101",
                address="123 Main St, Charlotte, NC",
                order_type="Delivery",
                order_date=datetime.now() - timedelta(days=3),
                description="No onions please",
                total_price=15.48,
                promotion_id=promo_map["WELCOME10"],
                order_status="Delivered",
            ),
            Order(
                customer_name="Bob Smith",
                email="bob@example.com",
                phone="704-555-0102",
                order_type="Pickup",
                order_date=datetime.now() - timedelta(days=1),
                description="Extra napkins",
                total_price=8.49,
                order_status="Preparing",
            ),
            Order(
                customer_name="Carol Davis",
                email="carol@example.com",
                phone="704-555-0103",
                address="456 Oak Ave, Charlotte, NC",
                order_type="Delivery",
                order_date=datetime.now(),
                description="Ring doorbell on arrival",
                total_price=12.48,
                order_status="Pending",
            ),
            Order(
                customer_name="Dave Wilson",
                phone="704-555-0104",
                order_type="Pickup",
                order_date=datetime.now() - timedelta(days=7),
                total_price=5.49,
                order_status="Completed",
            ),
        ]
        db.add_all(orders)
        db.flush()

        # 7. Order Details (items in each order)
        order_details = [
            # Alice: BLT + Turkey Club
            OrderDetail(order_id=orders[0].id, sandwich_id=sand_map["BLT"], amount=1),
            OrderDetail(order_id=orders[0].id, sandwich_id=sand_map["Turkey Club"], amount=1),
            # Bob: Turkey Club
            OrderDetail(order_id=orders[1].id, sandwich_id=sand_map["Turkey Club"], amount=1),
            # Carol: Grilled Cheese x2
            OrderDetail(order_id=orders[2].id, sandwich_id=sand_map["Grilled Cheese"], amount=2),
            # Dave: Grilled Cheese
            OrderDetail(order_id=orders[3].id, sandwich_id=sand_map["Grilled Cheese"], amount=1),
        ]
        db.add_all(order_details)
        db.flush()

        # 8. Payments (one per order)
        payments = [
            Payment(order_id=orders[0].id, payment_type="Credit Card", transaction_status="completed", card_number="4242", payment_amount=15.48),
            Payment(order_id=orders[1].id, payment_type="Debit Card", transaction_status="completed", card_number="1234", payment_amount=8.49),
            Payment(order_id=orders[2].id, payment_type="Credit Card", transaction_status="pending", card_number="5678", payment_amount=12.48),
            Payment(order_id=orders[3].id, payment_type="Cash", transaction_status="completed", payment_amount=5.49),
        ]
        db.add_all(payments)
        db.flush()

        # 9. Reviews
        reviews = [
            Review(order_id=orders[0].id, menu_item_id=menu_map["BLT"], customer_name="Alice Johnson", rating=5, review_text="Best BLT I've ever had!"),
            Review(order_id=orders[0].id, menu_item_id=menu_map["Turkey Club"], customer_name="Alice Johnson", rating=4, review_text="Great club sandwich, a bit heavy on the mayo."),
            Review(order_id=orders[3].id, menu_item_id=menu_map["Grilled Cheese"], customer_name="Dave Wilson", rating=3, review_text="Good but could use more cheese."),
        ]
        db.add_all(reviews)

        db.commit()
        print("[SEEDER] Mock data seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"[SEEDER] ERROR: {e}")
    finally:
        db.close()
