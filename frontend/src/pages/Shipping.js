import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import axios from "axios";
import Modal from "../components/Modal"; // Importa el modal

const Shipping = ({ cart, setCart }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    shipping_street: "",
    commune: "",
    phone: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quote, setQuote] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false); // Estado del modal

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setQuote(null);
    setError(null);
    setIsModalOpen(true); // **Abre el modal inmediatamente**

    if (!cart) {
      setError("No hay productos en el carrito.");
      setLoading(false);
      return;
    }

    console.log("cartcurrentprod", cart.products);

    const productsArray = cart?.products?.map((item) => ({
      productId: item.id,
      price: item.price,
      quantity: item.quantity,
      discount: item.discountPercentage || 0,
    })) || [];

    const requestData = {
      products: productsArray,
      customer_data: formData,
    };

    try {
      const response = await axios.post(
        "http://localhost:8000/api/cart",
        requestData
      );
      setQuote(response.data); // Guarda la cotización
    } catch (error) {
      setError("No hay envíos disponibles :(");
    } finally {
      setLoading(false); // Detiene el spinner
    }
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold mb-6">Cotizar despacho</h2>
      
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
        <label className="block mb-2">
          Nombre:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            required
          />
        </label>

        <label className="block mb-2">
          Dirección:
          <input
            type="text"
            name="shipping_street"
            value={formData.shipping_street}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            required
          />
        </label>

        <label className="block mb-2">
          Comuna:
          <input
            type="text"
            name="commune"
            value={formData.commune}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            required
          />
        </label>

        <label className="block mb-2">
          Teléfono:
          <input
            type="text"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            required
          />
        </label>

        <div className="mt-6 flex space-x-4">
          <Button type="submit" className="bg-green-500" disabled={loading}>
            {loading ? "Cotizando..." : "Cotizar"}
          </Button>
          <Button onClick={() => navigate("/checkout")}>Volver</Button>
        </div>
      </form>

      {/* Modal con estado de carga y cotización */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        quote={quote}
        loading={loading}
      />
    </div>
  );
};

export default Shipping;
