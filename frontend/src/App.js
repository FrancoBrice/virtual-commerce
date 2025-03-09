import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Checkout from "./pages/Checkout";
import Shipping from "./pages/Shipping";

function App() {
  const [cart, setCart] = useState({ products: [], customer_data: {} });


  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home cart={cart} setCart={setCart} />} />
        <Route path="/checkout" element={<Checkout cart={cart} setCart={setCart} />} />
        <Route path="/shipping" element={<Shipping cart={cart} setCart={setCart} />} />
      </Routes>
    </Router>
  );
}

export default App;
