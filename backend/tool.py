from langchain_core.tools import tool
from database import get_database
import os

@tool
def purchase_price(quantity: int, item: str) -> int:
    """
    Calculate total purchase price of an item given it's quantity
    """
    db = get_database()
    collection = db[os.getenv('COLLECTION')]

    item_details = collection.find({"product_name": item})
    
    price = item_details[0]['product_price']

    total_purchase_price = price * quantity

    return total_purchase_price

# @tool
# def pay(total_price: int) -> str:
#     """
#     Initiate the 
#     """
