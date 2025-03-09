import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button";

const Checkout = ({ cart, setCart }) => {
  const navigate = useNavigate();

  const clearCart = () => {
    setCart(null);
    navigate("/");
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold mb-6">Resumen del Carrito</h2>

      {cart.products.map((item) => (
        <div key={item.id} className="flex items-center justify-between p-4 bg-white shadow-md rounded-md mb-4">
          <img src={item.thumbnail} alt={item.title} className="w-16 h-16 rounded-md" />
          <div className="flex-1 ml-4">
            <p className="text-lg font-semibold">{item.title}</p>
            <p className="text-gray-600">Cantidad: {item.quantity}</p>
            <p className="text-gray-600">Precio: ${item.price}</p>
          </div>
        </div>
      ))}

      <div className="mt-6 flex space-x-4">
        <Button onClick={clearCart} className="bg-red-500">Limpiar carrito</Button>
        <Button onClick={() => navigate("/")}>Volver</Button>
        <Button onClick={() => navigate("/shipping")} className="bg-blue-500">Cotizar despacho</Button>
      </div>
    </div>
  );
};

export default Checkout;
