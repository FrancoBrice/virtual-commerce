import React from 'react';

const Button = ({ onClick, children, className = '', ...props }) => {
  return (
    <button
      onClick={onClick}
      className={`${className} px-4 py-2 bg-blue-500 rounded hover:bg-blue-600`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
