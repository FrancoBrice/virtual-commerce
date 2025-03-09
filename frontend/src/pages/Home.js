import React, { useState } from "react";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { isCartValid } from "../utils/cartUtils";

const Home = ({ cart, setCart }) => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");

  const fetchCart = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/generate-random-cart");
      console.log("Carrito generado:", response.data);
      setCart(response.data);
      setMessage("Carrito generado con éxito. ¡Listo para avanzar!");
    } catch (error) {
      console.error("Error al obtener el carrito:", error);
      setMessage("Hubo un error al generar el carrito.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-6 text-center">
      <h1 className="text-5xl sm:text-7xl font-bold text-gray-900 mb-6">
        Tienda Flapp
      </h1>

      <div className="h-8 mb-6">
        {!isCartValid(cart) && !message && (
          <p className="text-gray-600 text-lg">
            Genera un carrito para continuar.
          </p>
        )}
        {message && (
          <p className="text-green-600 text-lg font-medium">
            {message}
          </p>
        )}
      </div>

      <div className="mt-4 flex flex-col items-center space-y-4 w-full max-w-md">
        <Button 
          onClick={fetchCart} 
          className="w-full bg-blue-500 hover:bg-blue-600 px-6 py-3 text-white text-lg rounded-md shadow-md"
        >
          Generar Carrito
        </Button>
        
        <Button
          onClick={() => navigate("/checkout")}
          disabled={!isCartValid(cart)}
          className={`w-full px-6 py-3 text-lg rounded-md shadow-md transition-opacity ${
            isCartValid(cart) ? "bg-green-500 hover:bg-green-600 text-white" : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          Finalizar Compra
        </Button>
      </div>
    </div>
  );
};

export default Home;
