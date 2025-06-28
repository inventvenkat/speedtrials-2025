import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

const Input: React.FC<InputProps> = ({ className, ...props }) => {
  return (
    <input
      className={`border border-gray-300 rounded-full p-2 pl-10 w-full ${className}`}
      {...props}
    />
  );
};

export default Input;
