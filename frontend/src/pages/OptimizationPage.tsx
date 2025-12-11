import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { 
  CpuChipIcon, 
  Cog6ToothIcon, 
  PlayIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';

const OptimizationPage: React.FC = () => {
  const [selectedSolver, setSelectedSolver] = useState('classical');
  const [isRunning, setIsRunning] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [progress, setProgress] = useState(0);
  const [budget, setBudget] = useState(1000000);
  const [maxAssets, setMaxAssets] = useState(15);
  const [riskAversion, setRiskAversion] = useState(1.0);
  const [discretization, setDiscretization] = useState(20);
  const navigate = useNavigate();

  const solvers = [
    {
      id: 'classical',
      name: 'Classical Optimizer',
      description: 'Traditional Markowitz mean-variance optimization with CVXPY',
      icon: '📊',
      complexity: 'Low',
      speed: 'Fast'
    },
    {
      id: 'qubo',
      name: 'QUBO Solver',
      description: 'Quadratic Unconstrained Binary Optimization with simulated annealing',
      icon: '🔢',
      complexity: 'Medium',
      speed: 'Medium'
    },
    {
      id: 'qaoa',
      name: 'QAOA Quantum',
      description: 'Quantum Approximate Optimization Algorithm using Qiskit',
      icon: '⚛️',
      complexity: 'High',
      speed: 'Slow'
    }
  ];

  const handleRunOptimization = async () => {
    setShowModal(true);
    setIsRunning(true);
    setProgress(0);

    try {
      // Get selected dataset ID from localStorage
      const selectedDatasetId = parseInt(localStorage.getItem('selectedDatasetId') || '-1');
      
      // Prepare optimization request
      const optimizationRequest = {
        solver: selectedSolver,
        dataset_id: selectedDatasetId,
        constraints: {
          budget: budget,
          max_assets: maxAssets,
          max_weight_per_asset: 1.0,
          risk_aversion: riskAversion,
          discretization: discretization,
          allow_short_selling: false
        },
        solver_params: {
          p_layers: 1,
          learning_rate: 0.1,
          shots: 1024,
          max_iterations: 100,
          num_reads: 1000,
          solver: "ECOS",
          verbose: false
        },
        experiment_name: `${selectedSolver}_optimization_${Date.now()}`
      };

      // Start optimization (use sample endpoint for sample datasets)
      const response = optimizationRequest.dataset_id < 0 
        ? await apiService.runSampleOptimization(optimizationRequest)
        : await apiService.runOptimization(optimizationRequest);
      
      if (response.data) {
        // Simulate progress while waiting for results
        const interval = setInterval(() => {
          setProgress(prev => {
            if (prev >= 90) {
              clearInterval(interval);
              return 90;
            }
            return prev + Math.random() * 10;
          });
        }, 500);

        // Poll for job completion (simplified for demo)
        setTimeout(async () => {
          clearInterval(interval);
          setProgress(100);
          setIsRunning(false);
          
          setTimeout(() => {
            setShowModal(false);
            navigate('/results');
          }, 1500);
        }, 3000);
      } else {
        throw new Error(response.error || 'Optimization failed');
      }
    } catch (error) {
      console.error('Optimization error:', error);
      setIsRunning(false);
      setProgress(0);
      alert('Optimization failed. Please try again.');
      setTimeout(() => setShowModal(false), 1000);
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
          className="text-center mb-12"
        >
          <h1 className="heading-1 text-text-primary mb-4">Portfolio Optimization</h1>
          <p className="text-xl text-text-secondary max-w-3xl mx-auto">
            Configure your optimization parameters and choose between classical and quantum algorithms
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Sidebar - Configuration */}
          <div className="lg:col-span-1 space-y-6">
            {/* Solver Selection */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="glass-card"
            >
              <h2 className="section-title text-text-primary mb-6 flex items-center">
                <CpuChipIcon className="w-6 h-6 mr-2 text-quantum-blue" />
                Choose Solver
              </h2>
              
              <div className="space-y-3">
                {solvers.map((solver) => (
                  <div
                    key={solver.id}
                    className={`p-4 rounded-lg border cursor-pointer transition-all duration-200 hover-lift ${
                      selectedSolver === solver.id
                        ? 'border-quantum-blue bg-quantum-blue/10'
                        : 'border-white/10 hover:border-quantum-blue/30'
                    }`}
                    onClick={() => setSelectedSolver(solver.id)}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{solver.icon}</span>
                        <span className="font-medium text-text-primary">{solver.name}</span>
                      </div>
                      {selectedSolver === solver.id && (
                        <div className="w-3 h-3 bg-quantum-blue rounded-full"></div>
                      )}
                    </div>
                    <p className="text-sm text-text-secondary mb-3">{solver.description}</p>
                    <div className="flex justify-between text-xs text-text-muted">
                      <span>Complexity: {solver.complexity}</span>
                      <span>Speed: {solver.speed}</span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Constraints */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="glass-card"
            >
              <h2 className="section-title text-text-primary mb-6 flex items-center">
                <Cog6ToothIcon className="w-6 h-6 mr-2 text-quantum-blue" />
                Constraints
              </h2>
              
              <div className="space-y-6">
                {/* Budget */}
                <div>
                  <label className="block text-text-primary font-medium mb-2">
                    Budget ($)
                  </label>
                  <input
                    type="number"
                    className="input-quantum w-full"
                    placeholder="1000000"
                    value={budget}
                    onChange={(e) => setBudget(Number(e.target.value))}
                  />
                </div>

                {/* Max Assets */}
                <div>
                  <label className="block text-text-primary font-medium mb-2">
                    Maximum Assets
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="30"
                    value={maxAssets}
                    onChange={(e) => setMaxAssets(Number(e.target.value))}
                    className="slider-quantum"
                  />
                  <div className="flex justify-between text-sm text-text-muted mt-1">
                    <span>5</span>
                    <span>{maxAssets}</span>
                    <span>30</span>
                  </div>
                </div>

                {/* Risk Aversion */}
                <div>
                  <label className="block text-text-primary font-medium mb-2">
                    Risk Aversion (λ)
                  </label>
                  <input
                    type="range"
                    min="0.1"
                    max="2.0"
                    step="0.1"
                    value={riskAversion}
                    onChange={(e) => setRiskAversion(Number(e.target.value))}
                    className="slider-quantum"
                  />
                  <div className="flex justify-between text-sm text-text-muted mt-1">
                    <span>0.1</span>
                    <span>{riskAversion}</span>
                    <span>2.0</span>
                  </div>
                </div>

                {/* Weight Discretization */}
                <div>
                  <label className="block text-text-primary font-medium mb-2">
                    Weight Discretization
                  </label>
                  <select 
                    className="input-quantum w-full"
                    value={discretization}
                    onChange={(e) => setDiscretization(Number(e.target.value))}
                  >
                    <option value="10">10 levels</option>
                    <option value="20">20 levels</option>
                    <option value="50">50 levels</option>
                    <option value="100">100 levels</option>
                  </select>
                </div>
              </div>
            </motion.div>

            {/* Run Button */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <button
                onClick={handleRunOptimization}
                disabled={isRunning}
                className="btn-primary w-full flex items-center justify-center space-x-2 py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <PlayIcon className="w-6 h-6" />
                <span>{isRunning ? 'Running...' : 'Run Optimization'}</span>
              </button>
            </motion.div>
          </div>

          {/* Right Panel - Info & Preview */}
          <div className="lg:col-span-2 space-y-6">
            {/* Solver Info */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="glass-card"
            >
              <div className="flex items-center mb-4">
                <InformationCircleIcon className="w-6 h-6 text-quantum-blue mr-2" />
                <h2 className="section-title text-text-primary">
                  {solvers.find(s => s.id === selectedSolver)?.name} Details
                </h2>
              </div>
              
              <div className="prose prose-invert max-w-none">
                {selectedSolver === 'classical' && (
                  <div>
                    <p className="text-text-secondary mb-4">
                      The classical optimizer uses the Markowitz mean-variance framework to find the optimal 
                      portfolio allocation. It solves a quadratic programming problem to maximize expected 
                      return while minimizing risk.
                    </p>
                    <div className="bg-white/5 p-4 rounded-lg">
                      <h4 className="text-text-primary font-medium mb-2">Algorithm Details:</h4>
                      <ul className="text-text-secondary text-sm space-y-1">
                        <li>• Convex optimization using CVXPY</li>
                        <li>• Supports linear and quadratic constraints</li>
                        <li>• Guaranteed global optimum</li>
                        <li>• Fast execution (typically &lt; 1 second)</li>
                      </ul>
                    </div>
                  </div>
                )}
                
                {selectedSolver === 'qubo' && (
                  <div>
                    <p className="text-text-secondary mb-4">
                      QUBO (Quadratic Unconstrained Binary Optimization) formulation converts the portfolio 
                      problem into a binary optimization problem that can be solved using quantum-inspired 
                      algorithms.
                    </p>
                    <div className="bg-white/5 p-4 rounded-lg">
                      <h4 className="text-text-primary font-medium mb-2">Algorithm Details:</h4>
                      <ul className="text-text-secondary text-sm space-y-1">
                        <li>• Binary variable encoding for asset weights</li>
                        <li>• Penalty terms for constraint enforcement</li>
                        <li>• Simulated annealing solver</li>
                        <li>• Good approximation quality</li>
                      </ul>
                    </div>
                  </div>
                )}
                
                {selectedSolver === 'qaoa' && (
                  <div>
                    <p className="text-text-secondary mb-4">
                      QAOA (Quantum Approximate Optimization Algorithm) uses quantum circuits to explore 
                      the solution space more efficiently than classical algorithms for certain problem types.
                    </p>
                    <div className="bg-white/5 p-4 rounded-lg">
                      <h4 className="text-text-primary font-medium mb-2">Algorithm Details:</h4>
                      <ul className="text-text-secondary text-sm space-y-1">
                        <li>• Quantum circuit with parameterized gates</li>
                        <li>• Variational quantum eigensolver approach</li>
                        <li>• Qiskit simulator backend</li>
                        <li>• Potential quantum advantage</li>
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Quantum Circuit Preview */}
            {selectedSolver === 'qaoa' && (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="glass-card"
              >
                <h2 className="section-title text-text-primary mb-6">Quantum Circuit Preview</h2>
                
                <div className="bg-white/5 p-6 rounded-lg">
                  <div className="space-y-4">
                    {/* Circuit visualization */}
                    {[0, 1, 2, 3].map((qubit) => (
                      <div key={qubit} className="flex items-center space-x-4">
                        <span className="text-text-muted text-sm w-8">q{qubit}</span>
                        <div className="flex-1 flex items-center space-x-2">
                          <div className="h-0.5 bg-text-muted flex-1"></div>
                          <div className="w-8 h-8 border-2 border-quantum-blue rounded-lg flex items-center justify-center">
                            <span className="text-xs text-quantum-blue font-bold">H</span>
                          </div>
                          <div className="h-0.5 bg-text-muted w-16"></div>
                          <div className="w-8 h-8 border-2 border-quantum-sky rounded-lg flex items-center justify-center">
                            <span className="text-xs text-quantum-sky font-bold">RZ</span>
                          </div>
                          <div className="h-0.5 bg-text-muted flex-1"></div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 text-center">
                    <span className="text-text-muted text-sm">
                      Circuit depth: 2 | Gates: 8 | Parameters: 4
                    </span>
                  </div>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Optimization Modal */}
        <AnimatePresence>
          {showModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="modal-overlay"
              onClick={() => !isRunning && setShowModal(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="modal-content max-w-md"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-xl font-semibold text-text-primary">
                    Running Optimization
                  </h3>
                  {!isRunning && (
                    <button
                      onClick={() => setShowModal(false)}
                      className="text-text-muted hover:text-text-primary"
                    >
                      <XMarkIcon className="w-6 h-6" />
                    </button>
                  )}
                </div>

                <div className="text-center">
                  <div className="quantum-loader mx-auto mb-6"></div>
                  
                  <div className="progress-bar mb-4">
                    <div 
                      className="progress-fill"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                  
                  <p className="text-text-secondary mb-2">
                    {isRunning ? 'Optimizing portfolio...' : 'Optimization complete!'}
                  </p>
                  <p className="text-sm text-text-muted">
                    {Math.round(progress)}% complete
                  </p>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default OptimizationPage;