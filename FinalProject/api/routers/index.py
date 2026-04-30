from . import orders, order_details, menu, sandwiches, recipes, resources, payments, promotions, reviews, tracking


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(menu.router)
    app.include_router(sandwiches.router)
    app.include_router(recipes.router)
    app.include_router(resources.router)
    app.include_router(payments.router)
    app.include_router(promotions.router)
    app.include_router(reviews.router)
    app.include_router(tracking.router)
