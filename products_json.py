""""Module to Extract data from the database and save it to products_ratings.json"""
import json
from dbexport.models import Product
from products_csv import get_reviews_statement


session, reviews_statement = get_reviews_statement()

products = []
for product, review_count, avg_rating in session.query(
    Product, reviews_statement.c.review_count, reviews_statement.c.avg_rating
).outerjoin(reviews_statement, Product.id == reviews_statement.c.product_id):
    products.append(
        {
            "name": product.name,
            "level": product.level,
            "published": product.published,
            "created_on": str(product.created_on.date()),
            "review_count": review_count or 0,
            "avg_rating": round(float(avg_rating), 4) if avg_rating else 0,
        }
    )

with open("product_ratings.json", "w", encoding="UTF-8") as f:
    json.dump(products, f, indent=2)
