import React from 'react';

interface BadgeProps {
  children?: React.ReactNode;
  variant: 'success' | 'danger';
}

const Badge: React.FC<BadgeProps> = ({ children, variant }) => {
  const variants = {
    success: 'bg-success text-white',
    danger: 'bg-danger text-white',
  };

  return (
    <span className={`px-2 py-1 rounded-full text-sm font-semibold ${variants[variant]}`}>
      {children}
    </span>
  );
};

export default Badge;
