import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaExclamationCircle } from "react-icons/fa";

const modalVariants = {
  initial: { scale: 0.8, opacity: 0 },
  animate: { scale: 1, opacity: 1, transition: { duration: 0.3, ease: "easeOut" } },
  exit: { scale: 0.8, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
};

const ErrorModal = ({ isOpen, onClose, message }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50">
          <motion.div
            className="bg-white p-6 rounded-lg shadow-lg w-96 max-w-full text-center"
            initial="initial"
            animate="animate"
            exit="exit"
            variants={modalVariants}
          >
            <FaExclamationCircle className="text-red-500 text-6xl mx-auto mb-4" />
            <h2 className="text-xl font-bold mb-2 text-red-600">¡Error de Stock!</h2>
            <p className="text-gray-600">{message}</p>
            <button
              onClick={onClose}
              className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Cerrar
            </button>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default ErrorModal;
