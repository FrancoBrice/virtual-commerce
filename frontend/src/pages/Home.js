import React, { useState } from "react";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { isCartValid } from "../utils/cartUtils";

const API_URL = process.env.REACT_APP_API_URL

const Home = ({ cart, setCart }) => {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const fetchCart = async () => {
    setIsLoading(true); 
    setMessage(""); 

    try {
      const response = await axios.post(`${API_URL}/cart/random`);
      console.log("Carrito generado:", response.data);
      setCart(response.data);
      setMessage("Carrito generado con éxito. ¡Listo para avanzar!");
    } catch (error) {
      console.error("Error al obtener el carrito:", error);
      setMessage("Hubo un error al generar el carrito.");
    } finally {
      setIsLoading(false); 
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-6 text-center">
      <h1 className="text-5xl sm:text-7xl font-bold text-gray-900 mb-6">
        Tienda Flapp
      </h1>

      <div className="h-8 mb-6">
        {!isCartValid(cart) && !message && (
          <p className="text-gray-600 text-lg">Genera un carrito para continuar.</p>
        )}
        {message && <p className="text-green-600 text-lg font-medium">{message}</p>}
      </div>

      <div className="mt-4 flex flex-col items-center space-y-4 w-full max-w-md">
        <Button
          onClick={fetchCart}
          disabled={isLoading}
          className="w-full bg-blue-500 hover:bg-blue-600 px-6 py-3 text-white text-lg rounded-md shadow-md flex justify-center items-center"
        >
          {isLoading ? (
            <svg className="animate-spin h-5 w-5 mr-2 text-white" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8z"></path>
            </svg>
          ) : (
            "Generar Carrito"
          )}
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
