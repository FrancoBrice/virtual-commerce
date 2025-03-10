import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import Home from "./pages/Home";
import Checkout from "./pages/Checkout";
import Shipping from "./pages/Shipping";

const pageVariants = {
  initial: { scale: 0.95, opacity: 0 },
  animate: { scale: 1, opacity: 1, transition: { duration: 0.5 } },
  exit: { scale: 1.05, opacity: 0, transition: { duration: 0.3 } },
};

const AnimatedRoutes = ({ cart, setCart }) => {
  const location = useLocation();
  
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        initial="initial"
        animate="animate"
        exit="exit"
        variants={pageVariants}
      >
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<Home cart={cart} setCart={setCart} />} />
          <Route path="/checkout" element={<Checkout cart={cart} setCart={setCart} />} />
          <Route path="/shipping" element={<Shipping cart={cart} setCart={setCart} />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  );
};

function App() {
  const [cart, setCart] = useState(() => {
    const savedCart = localStorage.getItem("cart");
    return savedCart ? JSON.parse(savedCart) : { products: [], customer_data: {} };
  });

  useEffect(() => {
    localStorage.setItem("cart", JSON.stringify(cart));
  }, [cart]);

  return (
    <Router>
      <AnimatedRoutes cart={cart} setCart={setCart} />
    </Router>
  );
}

export default App;
