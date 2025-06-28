import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import Button from '../shared/Button';

const Navbar: React.FC = () => {
  const { token, role, logout } = useAuth();

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">
          GA Water
        </Link>
        <div>
          {token ? (
            <>
              {role === 'Operator' && (
                <Link to="/dashboard" className="mr-4">
                  Dashboard
                </Link>
              )}
              {role === 'Regulator' && (
                <Link to="/map" className="mr-4">
                  Map
                </Link>
              )}
              <Button onClick={logout} variant="secondary">
                Logout
              </Button>
            </>
          ) : (
            <Link to="/login">
              <Button>Login</Button>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
