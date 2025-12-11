import React from 'react';
import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  CpuChipIcon, 
  ChartBarIcon,
  CodeBracketIcon,
  AcademicCapIcon,
  HeartIcon
} from '@heroicons/react/24/outline';

const AboutPage: React.FC = () => {
  const techStack = [
    { name: 'React', icon: '⚛️', description: 'Modern UI framework' },
    { name: 'TypeScript', icon: '📘', description: 'Type-safe development' },
    { name: 'Tailwind CSS', icon: '🎨', description: 'Utility-first styling' },
    { name: 'Framer Motion', icon: '🎭', description: 'Smooth animations' },
    { name: 'FastAPI', icon: '🚀', description: 'High-performance backend' },
    { name: 'Python', icon: '🐍', description: 'Data science & ML' },
    { name: 'Qiskit', icon: '⚛️', description: 'Quantum computing' },
    { name: 'CVXPY', icon: '📊', description: 'Convex optimization' },
    { name: 'PostgreSQL', icon: '🐘', description: 'Reliable database' },
    { name: 'Redis', icon: '🔴', description: 'Fast caching' },
    { name: 'Docker', icon: '🐳', description: 'Containerization' },
    { name: 'NumPy', icon: '🔢', description: 'Numerical computing' }
  ];

  const features = [
    {
      icon: CpuChipIcon,
      title: 'Quantum-Classical Hybrid',
      description: 'Combines the best of both worlds - proven classical optimization methods with cutting-edge quantum algorithms for potentially superior results.'
    },
    {
      icon: ChartBarIcon,
      title: 'Advanced Analytics',
      description: 'Comprehensive risk metrics, efficient frontier analysis, backtesting, and performance comparison tools for informed decision making.'
    },
    {
      icon: SparklesIcon,
      title: 'Modern Interface',
      description: 'Beautiful, responsive design with smooth animations and intuitive user experience inspired by leading fintech platforms.'
    }
  ];

  return (
    <div className="min-h-screen pt-20 pb-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h1 className="heading-1 text-text-primary mb-6">
            About Quantum Portfolio
            <span className="text-quantum-blue"> Optimizer</span>
          </h1>
          <p className="text-xl text-text-secondary max-w-4xl mx-auto leading-relaxed">
            A cutting-edge portfolio optimization platform that harnesses the power of quantum computing 
            and classical algorithms to help you build better investment portfolios.
          </p>
        </motion.div>

        {/* Quantum Visualization */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="glass-card mb-16 relative overflow-hidden"
        >
          <div className="absolute inset-0 opacity-10">
            <svg className="w-full h-full" viewBox="0 0 800 400">
              {/* Quantum circuit background */}
              <defs>
                <linearGradient id="quantumGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#1A73E8" stopOpacity="0.3" />
                  <stop offset="50%" stopColor="#4FC3F7" stopOpacity="0.5" />
                  <stop offset="100%" stopColor="#0D47A1" stopOpacity="0.3" />
                </linearGradient>
              </defs>
              
              {/* Circuit lines */}
              {[100, 150, 200, 250, 300].map((y, i) => (
                <g key={i}>
                  <line x1="50" y1={y} x2="750" y2={y} stroke="url(#quantumGradient)" strokeWidth="2" />
                  {/* Gates */}
                  <rect x="150" y={y-15} width="30" height="30" fill="none" stroke="#1A73E8" strokeWidth="2" rx="5" />
                  <rect x="300" y={y-15} width="30" height="30" fill="none" stroke="#4FC3F7" strokeWidth="2" rx="5" />
                  <rect x="450" y={y-15} width="30" height="30" fill="none" stroke="#0D47A1" strokeWidth="2" rx="5" />
                  <circle cx="600" cy={y} r="10" fill="none" stroke="#1A73E8" strokeWidth="2" />
                </g>
              ))}
            </svg>
          </div>
          
          <div className="relative z-10 text-center py-16">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-24 h-24 mx-auto mb-6 border-4 border-quantum-blue rounded-full relative"
            >
              <div className="absolute inset-2 border-2 border-quantum-sky rounded-full"></div>
              <div className="absolute inset-4 bg-quantum-blue/20 rounded-full"></div>
            </motion.div>
            <h2 className="heading-2 text-text-primary mb-4">The Future of Portfolio Optimization</h2>
            <p className="text-text-secondary max-w-2xl mx-auto">
              By combining quantum-inspired algorithms with classical optimization techniques, 
              we're pushing the boundaries of what's possible in financial portfolio construction.
            </p>
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="heading-2 text-text-primary text-center mb-12">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 * index }}
                className="glass-card hover-glow group text-center"
              >
                <feature.icon className="w-16 h-16 text-quantum-blue mx-auto mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="section-title text-text-primary mb-3">{feature.title}</h3>
                <p className="text-text-secondary">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Tech Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="glass-card mb-16"
        >
          <div className="flex items-center mb-8">
            <CodeBracketIcon className="w-8 h-8 text-quantum-blue mr-3" />
            <h2 className="heading-2 text-text-primary">Technology Stack</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {techStack.map((tech, index) => (
              <motion.div
                key={tech.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                className="p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-all duration-200 hover-lift text-center"
              >
                <div className="text-3xl mb-2">{tech.icon}</div>
                <h3 className="text-text-primary font-medium mb-1">{tech.name}</h3>
                <p className="text-text-muted text-xs">{tech.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Story */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="glass-card mb-16"
        >
          <div className="flex items-center mb-6">
            <AcademicCapIcon className="w-8 h-8 text-quantum-blue mr-3" />
            <h2 className="heading-2 text-text-primary">Our Story</h2>
          </div>
          
          <div className="prose prose-invert max-w-none">
            <p className="text-text-secondary mb-4">
              The Quantum Portfolio Optimizer was born from the intersection of cutting-edge quantum computing 
              research and practical financial engineering. As quantum computers become more accessible, 
              we saw an opportunity to explore how quantum algorithms could enhance traditional portfolio optimization.
            </p>
            <p className="text-text-secondary mb-4">
              Our platform implements the Quantum Approximate Optimization Algorithm (QAOA) alongside 
              classical methods like Markowitz mean-variance optimization, allowing users to compare 
              and contrast different approaches to portfolio construction.
            </p>
            <p className="text-text-secondary">
              While quantum advantage in portfolio optimization is still an active area of research, 
              our platform provides a practical testbed for exploring these emerging technologies 
              in a real-world financial context.
            </p>
          </div>
        </motion.div>

        {/* Credits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0 }}
          className="text-center"
        >
          <div className="glass-panel p-8 rounded-quantum inline-block">
            <HeartIcon className="w-8 h-8 text-status-error mx-auto mb-4" />
            <p className="text-text-secondary mb-2">
              Built with passion for quantum computing and financial innovation
            </p>
            <p className="text-text-muted text-sm">
              © 2025 Quantum Portfolio Optimizer. Open source and educational use.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AboutPage;