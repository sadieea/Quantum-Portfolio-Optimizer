import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  CpuChipIcon, 
  ChartBarIcon, 
  ShieldCheckIcon,
  SparklesIcon,
  ArrowRightIcon,
  PlayIcon
} from '@heroicons/react/24/outline';

const LandingPage: React.FC = () => {
  const features = [
    {
      icon: CpuChipIcon,
      title: 'Quantum-Classical Hybrid',
      description: 'Combines traditional optimization with quantum-inspired algorithms for superior portfolio construction.'
    },
    {
      icon: ChartBarIcon,
      title: 'Advanced Analytics',
      description: 'Real-time risk metrics, efficient frontier analysis, and comprehensive backtesting capabilities.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Risk Management',
      description: 'Sophisticated constraint handling with CVaR optimization and multi-objective portfolio construction.'
    },
    {
      icon: SparklesIcon,
      title: 'AI-Powered Insights',
      description: 'Machine learning enhanced optimization with explainable AI for transparent decision making.'
    }
  ];

  const steps = [
    {
      number: '01',
      title: 'Upload Data',
      description: 'Import your historical asset data or use our curated datasets'
    },
    {
      number: '02',
      title: 'Configure Constraints',
      description: 'Set your risk preferences, budget limits, and optimization parameters'
    },
    {
      number: '03',
      title: 'Optimize & Compare',
      description: 'Run classical and quantum algorithms, then compare results'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="heading-1 text-text-primary mb-6">
                Quantum Portfolio
                <span className="text-quantum-blue"> Optimizer</span>
              </h1>
              <p className="text-xl text-text-secondary max-w-3xl mx-auto mb-12 leading-relaxed">
                AI + Quantum Hybrid Engine for Smarter Asset Allocation. 
                Harness the power of quantum computing and classical optimization 
                to build superior investment portfolios.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
            >
              <Link to="/dataset" className="btn-primary flex items-center space-x-2 group">
                <span>Start Optimization</span>
                <ArrowRightIcon className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <button className="btn-secondary flex items-center space-x-2">
                <PlayIcon className="w-5 h-5" />
                <span>View Demo</span>
              </button>
            </motion.div>

            {/* Hero Illustration */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="relative max-w-4xl mx-auto"
            >
              <div className="glass-panel p-8 rounded-quantum">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  {/* Quantum Circuit Visualization */}
                  <div className="col-span-2 space-y-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-quantum-blue rounded-full animate-pulse"></div>
                      <div className="h-1 bg-gradient-to-r from-quantum-blue to-transparent flex-1 rounded"></div>
                      <div className="w-8 h-8 border-2 border-quantum-sky rounded-lg flex items-center justify-center">
                        <div className="w-2 h-2 bg-quantum-sky rounded-full"></div>
                      </div>
                      <div className="h-1 bg-gradient-to-r from-quantum-sky to-transparent flex-1 rounded"></div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 bg-quantum-sky rounded-full animate-pulse" style={{ animationDelay: '0.5s' }}></div>
                      <div className="h-1 bg-gradient-to-r from-quantum-sky to-transparent flex-1 rounded"></div>
                      <div className="w-8 h-8 border-2 border-quantum-blue rounded-lg flex items-center justify-center">
                        <div className="w-2 h-2 bg-quantum-blue rounded-full"></div>
                      </div>
                      <div className="h-1 bg-gradient-to-r from-quantum-blue to-transparent flex-1 rounded"></div>
                    </div>
                  </div>
                  
                  {/* Financial Charts */}
                  <div className="col-span-2 space-y-2">
                    <div className="flex items-end space-x-1 h-16">
                      {[0.3, 0.7, 0.4, 0.9, 0.6, 0.8, 0.5].map((height, i) => (
                        <div
                          key={i}
                          className="bg-gradient-to-t from-quantum-blue to-quantum-sky rounded-sm flex-1 animate-pulse"
                          style={{ 
                            height: `${height * 100}%`,
                            animationDelay: `${i * 0.1}s`
                          }}
                        ></div>
                      ))}
                    </div>
                    <div className="text-xs text-text-muted text-center">Portfolio Weights</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="heading-2 text-text-primary mb-4">How It Works</h2>
            <p className="text-text-secondary max-w-2xl mx-auto">
              Three simple steps to optimize your portfolio using cutting-edge quantum-classical hybrid algorithms
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="glass-card text-center hover-glow"
              >
                <div className="text-4xl font-bold text-quantum-blue mb-4">{step.number}</div>
                <h3 className="section-title text-text-primary mb-3">{step.title}</h3>
                <p className="text-text-secondary">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="heading-2 text-text-primary mb-4">Why Quantum?</h2>
            <p className="text-text-secondary max-w-2xl mx-auto">
              Quantum-inspired algorithms can explore solution spaces more efficiently, 
              potentially finding better portfolio allocations than classical methods alone
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="glass-card hover-glow group"
              >
                <feature.icon className="w-12 h-12 text-quantum-blue mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="section-title text-text-primary mb-3">{feature.title}</h3>
                <p className="text-text-secondary text-sm">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="glass-card"
          >
            <h2 className="heading-2 text-text-primary mb-4">
              Ready to Optimize Your Portfolio?
            </h2>
            <p className="text-text-secondary mb-8 max-w-2xl mx-auto">
              Start building better portfolios today with our quantum-classical hybrid optimization engine. 
              Upload your data and see the difference quantum computing can make.
            </p>
            <Link to="/dataset" className="btn-primary inline-flex items-center space-x-2 group">
              <span>Get Started Now</span>
              <ArrowRightIcon className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;