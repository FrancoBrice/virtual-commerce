import React, { useState } from "react";
import axios from "axios";
import Modal from "../components/Modal";
import OrderSummary from "../components/OrderSummary";
import ShippingForm from "../components/ShippingForm";

const API_URL = process.env.REACT_APP_API_URL

const Shipping = ({ cart, setCart }) => {
  const [quote, setQuote] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isShippingAvailable, setIsShippingAvailable] = useState(true);

  const handleQuoteRequest = async (customerData) => {
    setLoading(true);
    setQuote(null);
    setIsModalOpen(true);
    setIsShippingAvailable(true); 

    const productsArray = cart.products.map((item) => ({
      productId: item.id,
      price: item.price,
      quantity: item.quantity,
      discount: item.discountPercentage || 0,
    }));

    try {
      const response = await axios.post(`${API_URL}/cart`, { products: productsArray, customer_data: customerData });

      if (!response.data || response.data.price === 0) {
        setIsShippingAvailable(false); 
      } else {
        setQuote(response.data);
      }
    } catch (error) {
      setQuote(null);
      setIsShippingAvailable(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 p-8 bg-gray-50 min-h-screen">
      <div className="w-full lg:w-2/3 lg:pr-6">
        <ShippingForm onQuoteRequest={handleQuoteRequest} loading={loading} />
      </div>

      <OrderSummary
        cart={cart}
        quote={quote}
        isShippingAvailable={isShippingAvailable} 
        showShippingButton={false}
        onPay={() => setCart({ products: [] })}
      />

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} quote={quote} loading={loading} />
    </div>
  );
};

export default Shipping;
