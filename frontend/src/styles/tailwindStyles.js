export const buttonStyles = {
  primary: "w-full bg-blue-500 text-white hover:bg-blue-600",
  disabled: "w-full bg-gray-300 text-gray-500 cursor-not-allowed",
  success: "w-full bg-green-500 text-white hover:bg-green-600",
  danger: "w-full bg-red-500 text-white hover:bg-red-600",
  return: "w-full bg-gray-200 text-black hover:bg-gray-300 mt-2",
  clearCartButton: "text-red-500 hover:text-red-700 text-xl",
};

export const modalStyles = {
  container: "fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm z-50",
  content: "bg-white p-6 rounded-lg shadow-lg w-96 max-w-full text-center",
  icon: {
    error: "text-red-500 text-6xl mx-auto mb-4",
    success: "text-green-500 text-6xl mx-auto mb-4",
  },
  title: "text-xl font-bold mb-2",
  message: "text-gray-600",
};

export const cartItemStyles = {
  container: "flex items-center bg-gray-100 rounded-lg p-4 shadow-sm",
  image: "w-16 h-16 object-cover rounded-lg mr-4",
  details: "flex-1",
  title: "text-lg font-medium",
  quantity: "text-sm text-gray-500",
  price: "text-lg font-bold",
};

export const summaryStyles = {
  container: "w-full lg:w-1/3 lg:max-w-sm bg-white p-6 shadow-lg rounded-lg",
  section: "flex justify-between text-lg",
  discount: "flex justify-between text-lg text-red-600",
  total: "flex justify-between text-lg font-bold mt-2",
};

export const commonStyles = {
  card: "p-4 bg-white shadow-md rounded-md mb-4",
  button: "px-4 py-2 rounded-md text-white font-semibold transition-all",
  tooltip: "absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity",
  pageContainer: "flex flex-col items-center justify-center min-h-screen bg-gray-50 px-6 text-center",
};
