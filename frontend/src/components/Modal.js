import React from "react";
import { motion, AnimatePresence } from "framer-motion";

const modalVariants = {
  initial: { scale: 0.8, opacity: 0 },
  animate: { scale: 1, opacity: 1, transition: { duration: 0.3, ease: "easeOut" } },
  exit: { scale: 0.8, opacity: 0, transition: { duration: 0.2, ease: "easeIn" } },
};

const Modal = ({ isOpen, onClose, quote, loading }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50">
          {/* 🎯 Solo animamos el modal, NO el fondo */}
          <motion.div
            className="bg-white p-6 rounded-lg shadow-lg w-96 max-w-full text-center"
            initial="initial"
            animate="animate"
            exit="exit"
            variants={modalVariants}
          >
            <h2 className="text-xl font-bold mb-4">
              {loading ? "Generando cotización..." : "Cotización de Envío"}
            </h2>

            {loading ? (
              <div className="flex justify-center items-center">
                <div className="w-10 h-10 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
              </div>
            ) : quote ? (
              <>
                <p className="text-gray-700">
                  Envío Flapp con <strong>{quote.courier}</strong> ⚡️ - ${quote.price.toFixed(2)}
                </p>
              </>
            ) : (
              <p className="text-red-600 font-semibold">No hay envíos disponibles :(</p>
            )}

            <button
              onClick={onClose}
              className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-300"
            >
              Cerrar
            </button>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export default Modal;
