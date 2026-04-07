import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf


app = FastAPI(
    openapi_tags=[
        {"name": "Orders", "description": "Create and manage customer orders."},
        {"name": "Order Details", "description": "Line items (sandwiches) on each order."},
        {"name": "Order Tracking", "description": "Look up or update order status by tracking id."},
        {"name": "Menu", "description": "Menu items available to customers and staff."},
        {"name": "Sandwiches", "description": "Sandwich products and pricing."},
        {"name": "Recipes", "description": "Ingredient amounts linking sandwiches to resources."},
        {"name": "Resources", "description": "Ingredients and inventory items."},
        {"name": "Payments", "description": "Payments linked to orders."},
        {"name": "Promotions", "description": "Discount codes and promotions."},
        {"name": "Reviews", "description": "Customer reviews."},
    ],
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)