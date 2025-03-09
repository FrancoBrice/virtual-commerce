import React, { useState } from "react";
import Button from "./Button";
import { useNavigate } from "react-router-dom";
import { FaCheckCircle } from "react-icons/fa";

const OrderSummary = ({ cart, quote, isShippingAvailable, onPay, showShippingButton }) => {
  const navigate = useNavigate();
  const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);
  const [isPaying, setIsPaying] = useState(false);

  const calculateTotalProducts = () => {
    return cart.products.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  const calculateFinalTotal = () => {
    return calculateTotalProducts() + (isShippingAvailable && quote?.price ? quote.price : 0);
  };

  const handlePayment = () => {
    setIsPaying(true);
    onPay();
    setIsSuccessModalOpen(true);
    setTimeout(() => navigate("/"), 2000);
  };

  return (
    <div className="w-full lg:w-1/3 lg:max-w-sm bg-white p-6 shadow-lg rounded-lg">

      <h3 className="text-2xl font-bold mb-4">Resumen de Pedido</h3>

      <div className="flex justify-between text-lg">
        <span>Productos</span>
        <span className="font-semibold">${calculateTotalProducts().toFixed(2)}</span>
      </div>

      {quote && (quote?.price > 0 || !isShippingAvailable) && (
        <div className="flex justify-between text-lg">
          <span>Envío</span>
          <span className="font-semibold">
            {isShippingAvailable ? `$${quote?.price?.toFixed(2)}` : "No disponible"}
          </span>
        </div>
      )}

      <div className="flex justify-between text-lg font-bold mt-2">
        <span>Total</span>
        <span>${calculateFinalTotal().toFixed(2)}</span>
      </div>

      <hr className="my-4" />

      {showShippingButton ? (
        <Button
          onClick={() => navigate("/shipping")}
          className="w-full bg-blue-500 hover:bg-blue-600"
        >
          Cotizar Despacho
        </Button>
      ) : (
        <Button
          onClick={handlePayment}
          className={`w-full transition-opacity ${
            isShippingAvailable && quote ? "bg-green-500 hover:bg-green-600" : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
          disabled={!isShippingAvailable || !quote || isPaying}
        >
          {isPaying ? "Procesando..." : "Pagar"}
        </Button>
      )}

      <Button 
        onClick={() => navigate("/")} 
        className="w-full bg-gray-200 text-gray-950 hover:bg-gray-300 mt-2"
      >
        Volver
      </Button>

      {isSuccessModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96 max-w-full text-center">
            <FaCheckCircle className="text-green-500 text-6xl mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">¡Pedido realizado con éxito! 🎉</h2>
            <p className="text-gray-600">Gracias por tu compra.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrderSummary;
