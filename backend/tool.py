from langchain_core.tools import tool
from database import get_database
import os
import stripe

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

@tool
def initiate_payment(total_purchase_price: int, item: str, quantity: int) -> str:
    """
    Initiates payment using Stripe. Use after getting total_purchase_price from purchase_price tool. 
    Returns Stripe checkout URL.
    """
    
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item},
                    'unit_amount': total_purchase_price * 100,  # Convert to cents
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=f"{os.getenv('FRONTEND_URL')}/success",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/cancel",
        )
        return session.url
    except Exception as e:
        return f"Payment Error: {str(e)}"