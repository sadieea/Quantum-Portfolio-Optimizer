import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ClockIcon, 
  MagnifyingGlassIcon,
  ArrowPathIcon,
  EyeIcon,
  TrashIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

const HistoryPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedExperiment, setSelectedExperiment] = useState<any>(null);

  const experiments = [
    {
      id: 'exp_001',
      timestamp: '2024-01-15 14:30:22',
      dataset: 'S&P 500 Sample',
      solver: 'Classical',
      assets: 30,
      return: '12.4%',
      risk: '8.7%',
      sharpe: '1.42',
      runtime: '0.3s',
      status: 'completed'
    },
    {
      id: 'exp_002',
      timestamp: '2024-01-15 14:25:18',
      dataset: 'S&P 500 Sample',
      solver: 'QAOA',
      assets: 30,
      return: '12.1%',
      risk: '8.9%',
      sharpe: '1.36',
      runtime: '15.4s',
      status: 'completed'
    },
    {
      id: 'exp_003',
      timestamp: '2024-01-15 14:20:45',
      dataset: 'Government Bonds',
      solver: 'QUBO',
      assets: 15,
      return: '6.8%',
      risk: '4.2%',
      sharpe: '1.62',
      runtime: '2.1s',
      status: 'completed'
    },
    {
      id: 'exp_004',
      timestamp: '2024-01-15 13:45:12',
      dataset: 'Mixed Portfolio',
      solver: 'Classical',
      assets: 25,
      return: '10.2%',
      risk: '7.1%',
      sharpe: '1.44',
      runtime: '0.4s',
      status: 'completed'
    },
    {
      id: 'exp_005',
      timestamp: '2024-01-15 13:30:08',
      dataset: 'S&P 500 Sample',
      solver: 'QAOA',
      assets: 30,
      return: '-',
      risk: '-',
      sharpe: '-',
      runtime: '-',
      status: 'failed'
    }
  ];

  const filteredExperiments = experiments.filter(exp =>
    exp.dataset.toLowerCase().includes(searchTerm.toLowerCase()) ||
    exp.solver.toLowerCase().includes(searchTerm.toLowerCase()) ||
    exp.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-status-success';
      case 'failed': return 'text-status-error';
      case 'running': return 'text-status-warning';
      default: return 'text-text-muted';
    }
  };

  const getSolverIcon = (solver: string) => {
    switch (solver) {
      case 'Classical': return '📊';
      case 'QUBO': return '🔢';
      case 'QAOA': return '⚛️';
      default: return '🔧';
    }
  };

  return (
    <div className="min-h-screen pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex justify-between items-center mb-8"
        >
          <div>
            <h1 className="heading-1 text-text-primary mb-4">Experiment History</h1>
            <p className="text-xl text-text-secondary">
              View and reproduce previous optimization runs
            </p>
          </div>
          
          {/* Search */}
          <div className="relative">
            <MagnifyingGlassIcon className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted" />
            <input
              type="text"
              placeholder="Search experiments..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-quantum pl-10 w-64"
            />
          </div>
        </motion.div>

        {/* Experiments List */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="glass-card"
        >
          <div className="flex items-center mb-6">
            <ClockIcon className="w-6 h-6 text-quantum-blue mr-2" />
            <h2 className="section-title text-text-primary">Recent Experiments</h2>
            <span className="ml-auto text-text-muted text-sm">
              {filteredExperiments.length} experiments
            </span>
          </div>

          <div className="space-y-3">
            {filteredExperiments.map((experiment, index) => (
              <motion.div
                key={experiment.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                className="p-4 rounded-lg border border-white/10 hover:border-quantum-blue/30 transition-all duration-200 hover-lift cursor-pointer"
                onClick={() => setSelectedExperiment(experiment)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="text-2xl">{getSolverIcon(experiment.solver)}</div>
                    <div>
                      <div className="flex items-center space-x-3 mb-1">
                        <span className="font-mono text-quantum-blue text-sm">
                          {experiment.id}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded-full ${getStatusColor(experiment.status)} bg-current/10`}>
                          {experiment.status}
                        </span>
                      </div>
                      <div className="text-text-primary font-medium mb-1">
                        {experiment.dataset} • {experiment.solver}
                      </div>
                      <div className="text-text-muted text-sm">
                        {experiment.timestamp} • {experiment.assets} assets
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-6">
                    {experiment.status === 'completed' && (
                      <>
                        <div className="text-center">
                          <div className="text-status-success font-medium">{experiment.return}</div>
                          <div className="text-text-muted text-xs">Return</div>
                        </div>
                        <div className="text-center">
                          <div className="text-quantum-blue font-medium">{experiment.sharpe}</div>
                          <div className="text-text-muted text-xs">Sharpe</div>
                        </div>
                        <div className="text-center">
                          <div className="text-text-secondary font-medium">{experiment.runtime}</div>
                          <div className="text-text-muted text-xs">Runtime</div>
                        </div>
                      </>
                    )}
                    
                    <div className="flex items-center space-x-2">
                      <button className="btn-ghost p-2">
                        <EyeIcon className="w-4 h-4" />
                      </button>
                      <button className="btn-ghost p-2">
                        <ArrowPathIcon className="w-4 h-4" />
                      </button>
                      <button className="btn-ghost p-2 text-status-error hover:text-status-error">
                        <TrashIcon className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {filteredExperiments.length === 0 && (
            <div className="text-center py-12">
              <ClockIcon className="w-16 h-16 text-text-muted mx-auto mb-4 opacity-50" />
              <p className="text-text-muted">No experiments found matching your search.</p>
            </div>
          )}
        </motion.div>

        {/* Experiment Detail Modal */}
        <AnimatePresence>
          {selectedExperiment && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="modal-overlay"
              onClick={() => setSelectedExperiment(null)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="modal-content max-w-4xl"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h3 className="text-2xl font-semibold text-text-primary mb-2">
                      Experiment Details
                    </h3>
                    <p className="text-text-secondary">
                      {selectedExperiment.id} • {selectedExperiment.timestamp}
                    </p>
                  </div>
                  <button
                    onClick={() => setSelectedExperiment(null)}
                    className="text-text-muted hover:text-text-primary"
                  >
                    <XMarkIcon className="w-6 h-6" />
                  </button>
                </div>

                <div className="grid md:grid-cols-2 gap-6 mb-6">
                  {/* Configuration */}
                  <div className="bg-white/5 p-4 rounded-lg">
                    <h4 className="font-medium text-text-primary mb-3">Configuration</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-text-muted">Dataset:</span>
                        <span className="text-text-primary">{selectedExperiment.dataset}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-text-muted">Solver:</span>
                        <span className="text-text-primary">{selectedExperiment.solver}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-text-muted">Assets:</span>
                        <span className="text-text-primary">{selectedExperiment.assets}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-text-muted">Status:</span>
                        <span className={getStatusColor(selectedExperiment.status)}>
                          {selectedExperiment.status}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Results */}
                  <div className="bg-white/5 p-4 rounded-lg">
                    <h4 className="font-medium text-text-primary mb-3">Results</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-text-muted">Expected Return:</span>
                        <span className="text-status-success font-medium">{selectedExperiment.return}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-text-muted">Risk (Volatility):</span>
                        <span className="text-quantum-blue font-medium">{selectedExperiment.risk}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-text-muted">Sharpe Ratio:</span>
                        <span className="text-quantum-sky font-medium">{selectedExperiment.sharpe}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-text-muted">Runtime:</span>
                        <span className="text-text-primary">{selectedExperiment.runtime}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end space-x-3">
                  <button className="btn-secondary">
                    View Full Results
                  </button>
                  <button className="btn-primary flex items-center space-x-2">
                    <ArrowPathIcon className="w-4 h-4" />
                    <span>Reproduce Run</span>
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default HistoryPage;