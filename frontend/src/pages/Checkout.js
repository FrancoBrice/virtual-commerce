import React from "react";
import { useNavigate } from "react-router-dom";
import { FaTrash } from "react-icons/fa"; 
import OrderSummary from "../components/OrderSummary";
import { buttonStyles, commonStyles, cartItemStyles } from "../styles/tailwindStyles"; 

const API_URL = process.env.REACT_APP_API_URL;

const Checkout = ({ cart, setCart }) => {
  const navigate = useNavigate();

  const clearCart = async () => {
    if (!cart.id) return;

    try {
      const response = await fetch(`${API_URL}/cart/${cart.id}`, { method: "DELETE" });

      if (!response.ok) throw new Error("Error al eliminar el carrito.");

      setCart({ products: [], customer_data: {} });
      localStorage.removeItem("cart");

      setTimeout(() => navigate("/"), 500);
    } catch (error) {
      console.error("Error eliminando el carrito:", error);
      alert("No se pudo eliminar el carrito. Inténtalo de nuevo.");
    }
  };

  const renderCartItems = () => {
    if (cart.products.length === 0) {
      return <p className="text-gray-600">El carrito está vacío.</p>;
    }

    return cart.products.map((item) => (
      <div key={item.id} className={commonStyles.card}>
        <img src={item.thumbnail} alt={item.title} className={cartItemStyles.image} />
        <div className="flex-1 ml-4">
          <p className={cartItemStyles.title}>{item.title}</p>
          <p className={cartItemStyles.quantity}>Cantidad: {item.quantity}</p>
          <p className={cartItemStyles.price}>Precio: ${item.price}</p>
        </div>
      </div>
    ));
  };

  return (
    <div className="flex flex-col lg:flex-row p-8 bg-gray-50 min-h-screen">
      <div className="w-full lg:w-2/3 lg:pr-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold">Resumen del Carrito</h2>
          <div className="relative group">
            <button onClick={clearCart} className={buttonStyles.clearCartButton}>
              <FaTrash />
            </button>
            <span className={commonStyles.tooltip}>Vaciar Carrito</span>
          </div>
        </div>
        {renderCartItems()}
      </div>

      <OrderSummary cart={cart} showShippingButton={true} />
    </div>
  );
};

export default Checkout;
