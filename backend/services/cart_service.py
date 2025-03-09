cart_memory = {}

def store_cart(cart_data):
    cart_memory["cart"] = cart_data

def get_cart():
    return cart_memory.get("cart")
