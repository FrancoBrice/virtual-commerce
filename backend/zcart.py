import math
import logging
from services import populate_db, courier_service

async def process_cart(cart_request):
    """
    Processes the cart request:
      - Retrieves product details from DummyJSON.
      - Logs and validates each product (computing real stock as floor(stock / rating)).
      - Verifies available stock for each product.
      - Calls courier services to get shipping quotes.
      - Returns the best (lowest price) quote.
    """
    # Retrieve all products from DummyJSON API
    all_products = await populate_db.get_all_products()

    processed_products = []
    # Process each product in the cart
    for item in cart_request.products:
        product = all_products.get(item.productId)
        if not product:
            raise ValueError(f"Product with ID {item.productId} not found.")
        # Extract product details
        name = product.get("title", "Unknown")
        stock = product.get("stock", 0)
        rating = product.get("rating", 1)  # Avoid division by zero (assume minimum rating of 1)
        # Compute real stock: floor(stock / rating)
        real_stock = math.floor(stock / rating)
        # Log product details
        logging.info(
            f"Product ID: {item.productId}, Name: {name}, Unit Price: {item.price}, "
            f"Discount: {item.discount}, Requested: {item.quantity}, Stock: {stock}, "
            f"Rating: {rating}, Real Stock: {real_stock}"
        )
        if item.quantity > real_stock:
            raise ValueError(f"Insufficient stock for product ID {item.productId}. "
                             f"Requested {item.quantity}, available {real_stock}.")
        # Prepare product information for courier services
        processed_products.append({
            "productId": item.productId,
            "name": name,
            "quantity": item.quantity,
            "price": item.price,
            "discount": item.discount
        })

    # Define destination information from customer data
    destination = {
        "name": cart_request.customer_data.name,
        "shipping_street": cart_request.customer_data.shipping_street,
        "commune": cart_request.customer_data.commune,
        "phone": cart_request.customer_data.phone
    }
    # Get the best courier quote
    quote = await courier_service.get_best_courier_quote(processed_products, destination)
    if not quote:
        raise ValueError("No shipping rates available for the requested shipment.")
    return quote
