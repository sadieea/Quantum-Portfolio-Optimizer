import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  ChartBarIcon, 
  ArrowTrendingUpIcon, 
  ShieldCheckIcon,
  CurrencyDollarIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';

const ResultsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('classical');

  const kpis = [
    {
      label: 'Expected Return',
      value: '12.4%',
      change: '+2.1%',
      icon: ArrowTrendingUpIcon,
      color: 'text-status-success'
    },
    {
      label: 'Volatility',
      value: '8.7%',
      change: '-1.3%',
      icon: ShieldCheckIcon,
      color: 'text-quantum-blue'
    },
    {
      label: 'Sharpe Ratio',
      value: '1.42',
      change: '+0.18',
      icon: ChartBarIcon,
      color: 'text-quantum-sky'
    },
    {
      label: 'CVaR (95%)',
      value: '15.2%',
      change: '-2.8%',
      icon: CurrencyDollarIcon,
      color: 'text-status-warning'
    }
  ];

  const portfolioWeights = [
    { asset: 'AAPL', classical: 15.2, quantum: 12.8, sector: 'Technology' },
    { asset: 'MSFT', classical: 12.8, quantum: 14.1, sector: 'Technology' },
    { asset: 'GOOGL', classical: 10.5, quantum: 11.2, sector: 'Technology' },
    { asset: 'AMZN', classical: 8.9, quantum: 9.8, sector: 'Consumer Disc.' },
    { asset: 'TSLA', classical: 6.2, quantum: 8.4, sector: 'Consumer Disc.' },
    { asset: 'JPM', classical: 7.8, quantum: 6.9, sector: 'Financials' },
    { asset: 'JNJ', classical: 9.1, quantum: 8.2, sector: 'Healthcare' },
    { asset: 'V', classical: 5.4, quantum: 6.8, sector: 'Financials' },
  ];

  const solutions = [
    {
      id: 'classical',
      name: 'Classical',
      return: '12.4%',
      risk: '8.7%',
      sharpe: '1.42',
      runtime: '0.3s'
    },
    {
      id: 'qubo',
      name: 'QUBO',
      return: '11.8%',
      risk: '9.1%',
      sharpe: '1.29',
      runtime: '2.1s'
    },
    {
      id: 'qaoa',
      name: 'QAOA',
      return: '12.1%',
      risk: '8.9%',
      sharpe: '1.36',
      runtime: '15.4s'
    }
  ];

  return (
    <div className="min-h-screen pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex justify-between items-center mb-12"
        >
          <div>
            <h1 className="heading-1 text-text-primary mb-4">Optimization Results</h1>
            <p className="text-xl text-text-secondary">
              Compare classical and quantum optimization results
            </p>
          </div>
          <button className="btn-primary flex items-center space-x-2">
            <ArrowDownTrayIcon className="w-5 h-5" />
            <span>Export Results</span>
          </button>
        </motion.div>

        {/* KPI Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {kpis.map((kpi, index) => (
            <motion.div
              key={kpi.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              className="kpi-card group"
            >
              <div className="flex items-center justify-between mb-3">
                <kpi.icon className={`w-6 h-6 ${kpi.color}`} />
                <span className={`text-sm ${kpi.change.startsWith('+') ? 'text-status-success' : 'text-status-error'}`}>
                  {kpi.change}
                </span>
              </div>
              <div className="kpi-value group-hover:animate-glow-pulse">{kpi.value}</div>
              <div className="kpi-label">{kpi.label}</div>
            </motion.div>
          ))}
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Portfolio Weights Chart */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="chart-container"
          >
            <h2 className="section-title text-text-primary mb-6">Portfolio Weights</h2>
            
            <div className="space-y-3">
              {portfolioWeights.map((item, index) => (
                <motion.div
                  key={item.asset}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="flex items-center space-x-4"
                >
                  <div className="w-16 text-sm font-mono text-quantum-blue">
                    {item.asset}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-quantum-blue to-quantum-sky transition-all duration-1000"
                          style={{ width: `${(item.classical / 20) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-text-muted w-12 text-right">
                        {item.classical}%
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-quantum-sky to-quantum-navy transition-all duration-1000"
                          style={{ width: `${(item.quantum / 20) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-text-muted w-12 text-right">
                        {item.quantum}%
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="flex items-center justify-center space-x-6 mt-6 pt-4 border-t border-white/10">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-quantum-blue rounded-full"></div>
                <span className="text-sm text-text-secondary">Classical</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-quantum-sky rounded-full"></div>
                <span className="text-sm text-text-secondary">Quantum</span>
              </div>
            </div>
          </motion.div>

          {/* Efficient Frontier */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="chart-container"
          >
            <h2 className="section-title text-text-primary mb-6">Efficient Frontier</h2>
            
            <div className="relative h-64 bg-white/5 rounded-lg p-4">
              {/* Mock efficient frontier curve */}
              <svg className="w-full h-full" viewBox="0 0 300 200">
                <defs>
                  <linearGradient id="frontierGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#1A73E8" stopOpacity="0.8" />
                    <stop offset="100%" stopColor="#4FC3F7" stopOpacity="0.8" />
                  </linearGradient>
                </defs>
                
                {/* Efficient frontier curve */}
                <path
                  d="M 50 150 Q 100 100 150 80 Q 200 70 250 75"
                  stroke="url(#frontierGradient)"
                  strokeWidth="3"
                  fill="none"
                  className="drop-shadow-lg"
                />
                
                {/* Solution points */}
                <circle cx="120" cy="90" r="6" fill="#1A73E8" className="animate-pulse" />
                <circle cx="140" cy="85" r="6" fill="#4FC3F7" className="animate-pulse" />
                <circle cx="160" cy="88" r="6" fill="#0D47A1" className="animate-pulse" />
                
                {/* Labels */}
                <text x="120" y="110" textAnchor="middle" className="text-xs fill-current text-text-primary">
                  Classical
                </text>
                <text x="140" y="105" textAnchor="middle" className="text-xs fill-current text-text-primary">
                  QAOA
                </text>
                <text x="160" y="108" textAnchor="middle" className="text-xs fill-current text-text-primary">
                  QUBO
                </text>
              </svg>
              
              <div className="absolute bottom-2 left-2 text-xs text-text-muted">
                Risk →
              </div>
              <div className="absolute top-2 left-2 text-xs text-text-muted transform -rotate-90 origin-left">
                Return →
              </div>
            </div>
          </motion.div>
        </div>

        {/* Solution Comparison */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="glass-card"
        >
          <h2 className="section-title text-text-primary mb-6">Solution Comparison</h2>
          
          {/* Tab Navigation */}
          <div className="flex space-x-1 mb-6 bg-white/5 p-1 rounded-lg">
            {solutions.map((solution) => (
              <button
                key={solution.id}
                onClick={() => setActiveTab(solution.id)}
                className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200 relative ${
                  activeTab === solution.id
                    ? 'text-quantum-blue bg-white/10'
                    : 'text-text-secondary hover:text-text-primary'
                }`}
              >
                {solution.name}
                {activeTab === solution.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-quantum-blue rounded-full"
                  />
                )}
              </button>
            ))}
          </div>

          {/* Comparison Table */}
          <div className="table-quantum">
            <table className="w-full">
              <thead>
                <tr>
                  <th>Metric</th>
                  <th>Classical</th>
                  <th>QUBO</th>
                  <th>QAOA</th>
                  <th>Best</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="font-medium">Expected Return</td>
                  <td className="text-status-success font-bold">12.4%</td>
                  <td>11.8%</td>
                  <td>12.1%</td>
                  <td className="text-quantum-blue">Classical</td>
                </tr>
                <tr>
                  <td className="font-medium">Volatility</td>
                  <td className="text-status-success font-bold">8.7%</td>
                  <td>9.1%</td>
                  <td>8.9%</td>
                  <td className="text-quantum-blue">Classical</td>
                </tr>
                <tr>
                  <td className="font-medium">Sharpe Ratio</td>
                  <td className="text-status-success font-bold">1.42</td>
                  <td>1.29</td>
                  <td>1.36</td>
                  <td className="text-quantum-blue">Classical</td>
                </tr>
                <tr>
                  <td className="font-medium">Runtime</td>
                  <td className="text-status-success font-bold">0.3s</td>
                  <td>2.1s</td>
                  <td>15.4s</td>
                  <td className="text-quantum-blue">Classical</td>
                </tr>
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ResultsPage;