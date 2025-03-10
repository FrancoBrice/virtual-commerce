import React from "react";
import { useNavigate } from "react-router-dom";
import { FaTrash } from "react-icons/fa"; 
import OrderSummary from "../components/OrderSummary";

const Checkout = ({ cart, setCart }) => {
  const navigate = useNavigate();

  const clearCart = async () => {
    if (!cart.id) return;
  
    try {
      const response = await fetch(`http://localhost:8000/api/cart/${cart.id}`, {
        method: "DELETE",
      });
  
      if (!response.ok) {
        throw new Error("Error al eliminar el carrito.");
      }
  
      setCart({ products: [], customer_data: {} });
      localStorage.removeItem("cart");
  
      setTimeout(() => {
        navigate("/");
      }, 500);
    } catch (error) {
      console.error("Error eliminando el carrito:", error);
      alert("No se pudo eliminar el carrito. Inténtalo de nuevo.");
    }
  };
  
  

  return (
    <div className="flex flex-col lg:flex-row p-8 bg-gray-50 min-h-screen">
      <div className="w-full lg:w-2/3 lg:pr-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold">Resumen del Carrito</h2>
          <div className="relative group">
            <button onClick={clearCart} className="text-red-500 hover:text-red-700 text-xl">
              <FaTrash />
            </button>
            <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">
              Vaciar Carrito
            </span>
          </div>
        </div>

        {cart.products.length > 0 ? (
          cart.products.map((item) => (
            <div key={item.id} className="flex items-center justify-between p-4 bg-white shadow-md rounded-md mb-4">
              <img src={item.thumbnail} alt={item.title} className="w-16 h-16 rounded-md" />
              <div className="flex-1 ml-4">
                <p className="text-lg font-semibold">{item.title}</p>
                <p className="text-gray-600">Cantidad: {item.quantity}</p>
                <p className="text-gray-600">Precio: ${item.price}</p>
              </div>
            </div>
          ))
        ) : (
          <p className="text-gray-600">El carrito está vacío.</p>
        )}
      </div>

      <OrderSummary cart={cart} showShippingButton={true} />
    </div>
  );
};

export default Checkout;
