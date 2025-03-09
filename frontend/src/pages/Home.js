import React from "react";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Home = ({ cart, setCart }) => {
  const navigate = useNavigate();

  const fetchCart = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/generate-random-cart");
      console.log("Carrito generado:", response.data);
      setCart(response.data);
    } catch (error) {
      console.error("Error al obtener el carrito:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <h1 className="text-3xl font-bold mb-8">Tienda Flapp</h1>
      <div className="space-x-4">
        <Button onClick={fetchCart}>Generar carrito</Button>
        <Button 
          onClick={() => navigate("/checkout")}
          disabled={!cart} // 🔥 Deshabilitado si no hay carrito
          className={`transition-opacity ${cart ? "opacity-100" : "opacity-50 cursor-not-allowed"}`}
        >
          Finalizar compra
        </Button>
      </div>
    </div>
  );
};

export default Home;
