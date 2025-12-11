import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  HomeIcon, 
  CircleStackIcon, 
  CpuChipIcon, 
  ChartBarIcon, 
  ClockIcon, 
  Cog6ToothIcon, 
  InformationCircleIcon,
  UserIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';

const Navigation: React.FC = () => {
  const location = useLocation();
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const { user, logout, isAuthenticated } = useAuth();

  const navItems = [
    { path: '/', label: 'Home', icon: HomeIcon },
    { path: '/dataset', label: 'Dataset', icon: CircleStackIcon },
    { path: '/optimize', label: 'Optimize', icon: CpuChipIcon },
    { path: '/results', label: 'Results', icon: ChartBarIcon },
    { path: '/history', label: 'History', icon: ClockIcon },
    { path: '/settings', label: 'Settings', icon: Cog6ToothIcon },
    { path: '/about', label: 'About', icon: InformationCircleIcon },
  ];

  return (
    <nav className="sticky top-0 z-40 glass-panel border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 hover-lift">
            <div className="relative">
              <div className="w-8 h-8 border-2 border-quantum-blue rounded-full animate-quantum-ring"></div>
              <div className="absolute inset-1 bg-quantum-blue/20 rounded-full"></div>
            </div>
            <span className="text-xl font-bold text-text-primary">
              Quantum Portfolio
            </span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link ${isActive ? 'active' : ''}`}
                  onMouseEnter={() => setHoveredItem(item.path)}
                  onMouseLeave={() => setHoveredItem(null)}
                >
                  <div className="flex items-center space-x-2 px-3 py-2 rounded-lg relative">
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                    
                    {/* Hover underline animation */}
                    {(isActive || hoveredItem === item.path) && (
                      <motion.div
                        className="absolute bottom-0 left-1/2 transform -translate-x-1/2 h-0.5 bg-quantum-blue rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: isActive ? '2rem' : '1.5rem' }}
                        transition={{ duration: 0.2 }}
                      />
                    )}
                  </div>
                </Link>
              );
            })}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2 text-text-secondary">
                  <UserIcon className="w-5 h-5" />
                  <span className="text-sm">{user?.name}</span>
                </div>
                <button
                  onClick={logout}
                  className="btn-ghost flex items-center space-x-2"
                >
                  <ArrowRightOnRectangleIcon className="w-5 h-5" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => {
                    setAuthMode('login');
                    setShowAuthModal(true);
                  }}
                  className="btn-ghost"
                >
                  Sign In
                </button>
                <button
                  onClick={() => {
                    setAuthMode('register');
                    setShowAuthModal(true);
                  }}
                  className="btn-primary"
                >
                  Sign Up
                </button>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button className="btn-ghost">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      <div className="md:hidden glass-panel border-t border-white/10">
        <div className="px-2 pt-2 pb-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-link ${isActive ? 'active' : ''} flex items-center space-x-3 px-3 py-2 rounded-lg w-full`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        initialMode={authMode}
      />
    </nav>
  );
};

export default Navigation;