from . import (
    orders,
    order_details,
    order_tracking,
    menu,
    sandwiches,
    recipes,
    resources,
    payments,
    promotions,
    reviews,
)


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(order_tracking.router)
    app.include_router(menu.router)
    app.include_router(menu.legacy_router)
    app.include_router(sandwiches.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(payments.router)
    app.include_router(promotions.router)
    app.include_router(reviews.router)
