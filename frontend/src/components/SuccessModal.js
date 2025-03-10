import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaCheckCircle } from "react-icons/fa";

const modalVariants = {
  initial: { scale: 0.8, opacity: 0 },
  animate: { scale: 1, opacity: 1, transition: { duration: 0.3, ease: "easeOut" } },
  exit: { scale: 0.8, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
};

const SuccessModal = ({ isOpen, onClose }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50">
          {/* 🎯 SOLO animamos la caja del modal */}
          <motion.div
            className="bg-white p-6 rounded-lg shadow-lg w-96 max-w-full text-center"
            initial="initial"
            animate="animate"
            exit="exit"
            variants={modalVariants}
          >
            <FaCheckCircle className="text-green-500 text-6xl mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2">¡Pedido realizado con éxito! 🎉</h2>
            <p className="text-gray-600">Gracias por tu compra.</p>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default SuccessModal;
