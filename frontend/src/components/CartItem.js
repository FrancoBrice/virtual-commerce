import React from "react";

const CartItem = ({ product }) => {
  return (
    <div className="flex items-center bg-gray-100 rounded-lg p-4 shadow-sm">
      <img src={product.thumbnail} alt={product.title} className="w-16 h-16 object-cover rounded-lg mr-4" />
      <div className="flex-1">
        <h3 className="text-lg font-medium">{product.title}</h3>
        <p className="text-sm text-gray-500">Cantidad: {product.quantity}</p>
      </div>
      <p className="text-lg font-bold">${product.discountedTotal.toFixed(2)}</p>
    </div>
  );
};

export default CartItem;
