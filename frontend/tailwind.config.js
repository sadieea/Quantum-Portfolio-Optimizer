/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
      colors: {
        // Quantum Portfolio Optimizer Color Palette
        quantum: {
          blue: '#1A73E8',
          navy: '#0D47A1',
          sky: '#4FC3F7',
        },
        cosmic: {
          navy: '#0B0F19',
          gradient: '#111625',
        },
        text: {
          primary: '#FFFFFF',
          secondary: '#A8B2D1',
          muted: '#6B7280',
        },
        status: {
          success: '#4CAF50',
          warning: '#FFC107',
          error: '#EF5350',
        },
        glass: {
          panel: 'rgba(255, 255, 255, 0.06)',
        }
      },
      borderRadius: {
        'quantum': '20px',
      },
      backdropBlur: {
        'quantum': '12px',
      },
      animation: {
        'fade-up': 'fadeUp 0.2s ease-out',
        'fade-scale': 'fadeScale 0.2s ease-out',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
        'quantum-ring': 'quantumRing 3s linear infinite',
        'slide-up': 'slideUp 0.3s ease-out',
        'count-up': 'countUp 1s ease-out',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeScale: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(26, 115, 232, 0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(26, 115, 232, 0.6)' },
        },
        quantumRing: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        countUp: {
          '0%': { opacity: '0', transform: 'scale(0.8)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
      boxShadow: {
        'quantum': '0 8px 32px rgba(26, 115, 232, 0.12)',
        'quantum-hover': '0 12px 48px rgba(26, 115, 232, 0.2)',
        'glass': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'inner-glow': 'inset 0 1px 0 rgba(255, 255, 255, 0.1)',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
    },
  },
  plugins: [],
}