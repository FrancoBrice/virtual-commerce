export const isCartValid = (cart) => {
  return cart && Array.isArray(cart.products) && cart.products.length > 0;
};
