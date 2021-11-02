""""Module to Extract data from the database and save it to products_ratings.csv"""
import csv
from sqlalchemy.sql import func
from dbexport.config import Session
from dbexport.models import Product, Review


csv_file = open("product_ratings.csv", mode="w", encoding="UTF-8")
fields = ["name", "level", "published", "created_on", "review_count", "avg_rating"]
csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
csv_writer.writeheader()


def get_reviews_statement():
    """Returns a sql statement that summarizes the reviews .

    Returns:
        tuble: session, review_statement
    """
    session = Session()
    reviews_statement = (
        session.query(
            Review.product_id,
            func.count("*").label("review_count"),
            func.avg(Review.rating).label("avg_rating"),
        )
        .group_by(Review.product_id)
        .subquery()
    )
    return session, reviews_statement


reviews_session, reviews_statement = get_reviews_statement()

for product, review_count, avg_rating in reviews_session.query(
    Product, reviews_statement.c.review_count, reviews_statement.c.avg_rating
).outerjoin(reviews_statement, Product.id == reviews_statement.c.product_id):
    csv_writer.writerow(
        {
            "name": product.name,
            "level": product.level,
            "published": product.published,
            "created_on": product.created_on.date(),
            "review_count": review_count or 0,
            "avg_rating": round(float(avg_rating), 4) if avg_rating else 0,
        }
    )

csv_file.close()
