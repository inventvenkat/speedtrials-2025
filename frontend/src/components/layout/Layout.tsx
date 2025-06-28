import React from 'react';
import Navbar from './Navbar';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-light font-sans">
      <Navbar />
      <main className="container mx-auto p-4">
        {children}
      </main>
      <footer className="bg-dark text-white p-4 text-center">
        <div className="container mx-auto">
          <p>&copy; 2025 Georgia Water Quality. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
