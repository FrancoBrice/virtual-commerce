import React, { useState } from "react";
import Button from "./Button";
import { useNavigate } from "react-router-dom";
import SuccessModal from "./SuccessModal";
import ErrorModal from "./ErrorModal"; 
import axios from "axios";

const OrderSummary = ({ cart, quote, isShippingAvailable, onPay, showShippingButton }) => {
  const navigate = useNavigate();
  const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);
  const [isErrorModalOpen, setIsErrorModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isPaying, setIsPaying] = useState(false);

  const calculateOriginalTotal = () => cart.total || 0;
  const calculateDiscountedTotal = () => cart.discountedTotal || 0;
  const calculateTotalDiscount = () => calculateOriginalTotal() - calculateDiscountedTotal();
  const calculateFinalTotal = () => {
    return calculateDiscountedTotal() + (isShippingAvailable && quote?.price ? quote.price : 0);
  };

  const handlePayment = () => {
    setIsPaying(true);
    onPay();
    setIsSuccessModalOpen(true);
    setTimeout(() => navigate("/"), 3000);
  };

  const handleShippingValidation = async () => {
    try {
      const response = await axios.post(
        `http://localhost:8000/api/validate-stock?cart_id=${cart.id}`
      );

      if (response.status === 200) {
        navigate("/shipping");
      }
    } catch (error) {
      setErrorMessage("No hay suficiente stock disponible para sus productos.");
      setIsErrorModalOpen(true);
    }
  };

  return (
    <div className="w-full lg:w-1/3 lg:max-w-sm bg-white p-6 shadow-lg rounded-lg">
      <h3 className="text-2xl font-bold mb-4">Resumen de Pedido</h3>

      <div className="flex justify-between text-lg">
        <span>Productos</span>
        <span className="font-semibold">${calculateOriginalTotal().toFixed(2)}</span>
      </div>

      <div className="flex justify-between text-lg text-red-600">
        <span>Descuento aplicado</span>
        <span>- ${calculateTotalDiscount().toFixed(2)}</span>
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
          onClick={handleShippingValidation}
          className="w-full bg-blue-500 hover:bg-blue-600"
        >
          Cotizar Despacho
        </Button>
      ) : (
        <Button
          onClick={handlePayment}
          className={`w-full transition-opacity ${
            isShippingAvailable && quote
              ? "bg-green-500 hover:bg-green-600"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
          disabled={!isShippingAvailable || !quote || isPaying}
        >
          {isPaying ? "Procesando..." : "Pagar"}
        </Button>
      )}

      <Button onClick={() => navigate("/")} className="w-full bg-gray-200 text-black hover:bg-gray-300 mt-2">
        Volver
      </Button>

      <SuccessModal isOpen={isSuccessModalOpen} onClose={() => setIsSuccessModalOpen(false)} />
      <ErrorModal
        isOpen={isErrorModalOpen}
        onClose={() => setIsErrorModalOpen(false)}
        message={errorMessage}
      />
    </div>
  );
};

export default OrderSummary;
