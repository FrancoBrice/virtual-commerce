import React, { useState } from "react";
import Button from "./Button";

const ShippingForm = ({ onQuoteRequest, loading }) => {
  const [formData, setFormData] = useState({
    name: "",
    shipping_street: "",
    commune: "",
    phone: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onQuoteRequest(formData); 
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-3xl font-bold mb-6">Cotizar Despacho</h2>

      <label className="block mb-4">
        <span className="text-gray-700 font-medium">Nombre</span>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          required
        />
      </label>

      <label className="block mb-4">
        <span className="text-gray-700 font-medium">Dirección</span>
        <input
          type="text"
          name="shipping_street"
          value={formData.shipping_street}
          onChange={handleChange}
          className="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          required
        />
      </label>

      <label className="block mb-4">
        <span className="text-gray-700 font-medium">Comuna</span>
        <input
          type="text"
          name="commune"
          value={formData.commune}
          onChange={handleChange}
          className="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          required
        />
      </label>

      <label className="block mb-4">
        <span className="text-gray-700 font-medium">Teléfono</span>
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          className="w-full mt-1 p-2 border rounded-md focus:ring-2 focus:ring-blue-500"
          required
        />
      </label>

      <div className="mt-6 flex space-x-4">
        <Button type="submit" className="w-full bg-blue-500 hover:bg-blue-600" disabled={loading}>
          {loading ? "Cotizando..." : "Cotizar despacho"}
        </Button>
      </div>
    </form>
  );
};

export default ShippingForm;
