import React, { useState } from "react";
import Button from "./Button";
import { useNavigate } from "react-router-dom";
import SuccessModal from "./SuccessModal";
import ErrorModal from "./ErrorModal";
import axios from "axios";
import { summaryStyles, buttonStyles } from "../styles/tailwindStyles";

const API_URL = process.env.REACT_APP_API_URL;

const OrderSummary = ({ cart, quote, isShippingAvailable, onPay, showShippingButton }) => {
  const navigate = useNavigate();
  const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);
  const [isErrorModalOpen, setIsErrorModalOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isPaying, setIsPaying] = useState(false);

  const calculateOriginalTotal = () => cart.total || 0;
  const calculateDiscountedTotal = () => cart.discountedTotal || 0;
  const calculateTotalDiscount = () => calculateOriginalTotal() - calculateDiscountedTotal();
  const calculateFinalTotal = () => calculateDiscountedTotal() + (isShippingAvailable && quote?.price ? quote.price : 0);

  const handlePayment = () => {
    setIsPaying(true);
    onPay();
    setIsSuccessModalOpen(true);
    setTimeout(() => navigate("/"), 3000);
  };

  const handleShippingValidation = async () => {
    const stockRequest = { products: cart.products.map(product => ({ productId: product.id, price: product.price, quantity: product.quantity })) };
    try {
      const response = await axios.post(`${API_URL}/validate-stock`, stockRequest);
      if (response.status === 200) navigate("/shipping");
    } catch (error) {
      setErrorMessage("No hay suficiente stock disponible para sus productos.");
      setIsErrorModalOpen(true);
    }
  };

  return (
    <div className={summaryStyles.container}>
      <h3 className="text-2xl font-bold mb-4">Resumen de Pedido</h3>
      <div className={summaryStyles.section}><span>Productos</span><span className="font-semibold">${calculateOriginalTotal().toFixed(2)}</span></div>
      <div className={summaryStyles.discount}><span>Descuento aplicado</span><span>- ${calculateTotalDiscount().toFixed(2)}</span></div>
      {quote && (quote?.price > 0 || !isShippingAvailable) && (
        <div className={summaryStyles.section}><span>Envío</span><span className="font-semibold">{isShippingAvailable ? `$${quote?.price?.toFixed(2)}` : "No disponible"}</span></div>
      )}
      <div className={summaryStyles.total}><span>Total</span><span>${calculateFinalTotal().toFixed(2)}</span></div>
      <hr className="my-4" />
      {showShippingButton ? (
        <Button onClick={handleShippingValidation} className={buttonStyles.primary}>Cotizar Despacho</Button>
      ) : (
        <Button onClick={handlePayment} className={isShippingAvailable && quote ? buttonStyles.success : buttonStyles.disabled} disabled={!isShippingAvailable || !quote || isPaying}>
          {isPaying ? "Procesando..." : "Pagar"}
        </Button>
      )}
      <Button onClick={() => navigate("/")} className={buttonStyles.return}>Volver</Button>
      <SuccessModal isOpen={isSuccessModalOpen} onClose={() => setIsSuccessModalOpen(false)} />
      <ErrorModal isOpen={isErrorModalOpen} onClose={() => setIsErrorModalOpen(false)} message={errorMessage} />
    </div>
  );
};

export default OrderSummary;
