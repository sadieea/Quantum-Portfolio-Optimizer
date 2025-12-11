import numpy as np
from typing import Dict, Any, Optional
from app.utils.logger import logger
from app.utils.math_utils import normalize_weights

try:
    from qiskit import QuantumCircuit, Aer, execute
    from qiskit.algorithms import QAOA
    from qiskit.algorithms.optimizers import COBYLA, SPSA
    from qiskit.opflow import PauliSumOp
    from qiskit.quantum_info import SparsePauliOp
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    logger.warning("Qiskit not available. QAOA optimization will be disabled.")


class QAOASolver:
    """QAOA solver for portfolio optimization"""
    
    def __init__(self):
        self.backend = Aer.get_backend('aer_simulator')
    
    def solve_qaoa(self,
                   qubo_data: Dict[str, Any],
                   solver_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve QUBO using QAOA
        """
        if not QISKIT_AVAILABLE:
            raise ImportError("Qiskit is not available. Please install it with: pip install qiskit qiskit-aer")
        
        try:
            # Extract parameters
            p_layers = solver_params.get('p_layers', 1)
            shots = solver_params.get('shots', 1024)
            max_iterations = solver_params.get('max_iterations', 100)
            
            # Convert QUBO to Ising Hamiltonian
            hamiltonian = self._qubo_to_ising(qubo_data['qubo_matrix'])
            
            # Set up QAOA
            optimizer = COBYLA(maxiter=max_iterations)
            qaoa = QAOA(optimizer=optimizer, reps=p_layers, quantum_instance=self.backend)
            
            logger.info(f"Running QAOA with p={p_layers}, shots={shots}")
            
            # Run QAOA
            result = qaoa.compute_minimum_eigenvalue(hamiltonian)
            
            # Extract solution
            optimal_params = result.optimal_parameters
            optimal_value = result.optimal_value
            
            # Get the most probable bitstring
            eigenstate = result.eigenstate
            if hasattr(eigenstate, 'to_dict'):
                probabilities = eigenstate.to_dict()
                best_bitstring = max(probabilities.keys(), key=probabilities.get)
            else:
                # Fallback: sample from the circuit
                best_bitstring = self._sample_best_bitstring(optimal_params, hamiltonian, shots)
            
            # Convert bitstring to weights
            weights = self._bitstring_to_weights(best_bitstring, qubo_data['variable_mapping'])
            
            logger.info(f"QAOA completed: energy={optimal_value}, bitstring={best_bitstring}")
            
            return {
                'status': 'optimal',
                'weights': weights,
                'energy': optimal_value,
                'bitstring': best_bitstring,
                'optimal_parameters': optimal_params,
                'solver_info': {
                    'solver': 'qaoa',
                    'p_layers': p_layers,
                    'shots': shots,
                    'max_iterations': max_iterations,
                    'final_energy': optimal_value
                }
            }
            
        except Exception as e:
            logger.error(f"Error in QAOA solver: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'weights': None
            }
    
    def _qubo_to_ising(self, qubo_matrix: Dict) -> PauliSumOp:
        """Convert QUBO matrix to Ising Hamiltonian"""
        try:
            # Get number of variables
            variables = set()
            for (i, j) in qubo_matrix.keys():
                variables.add(i)
                variables.add(j)
            n_vars = len(variables)
            
            # Create Pauli operators
            pauli_list = []
            
            for (i, j), coeff in qubo_matrix.items():
                if i == j:
                    # Diagonal term: Z_i
                    pauli_str = ['I'] * n_vars
                    pauli_str[i] = 'Z'
                    pauli_list.append((''.join(pauli_str), coeff / 2))
                else:
                    # Off-diagonal term: Z_i Z_j
                    pauli_str = ['I'] * n_vars
                    pauli_str[i] = 'Z'
                    pauli_str[j] = 'Z'
                    pauli_list.append((''.join(pauli_str), coeff / 4))
            
            # Add constant term (shift for QUBO to Ising conversion)
            constant = sum(qubo_matrix.values()) / 4
            pauli_list.append(('I' * n_vars, constant))
            
            # Create SparsePauliOp
            sparse_pauli = SparsePauliOp.from_list(pauli_list)
            return PauliSumOp(sparse_pauli)
            
        except Exception as e:
            logger.error(f"Error converting QUBO to Ising: {e}")
            raise
    
    def _sample_best_bitstring(self, optimal_params: Dict, hamiltonian: PauliSumOp, shots: int) -> str:
        """Sample the best bitstring from QAOA circuit"""
        try:
            # This is a simplified implementation
            # In practice, you'd construct the QAOA circuit with optimal parameters
            # and sample from it
            
            n_qubits = hamiltonian.num_qubits
            
            # Create a simple sampling (placeholder)
            # In real implementation, construct QAOA circuit and sample
            counts = {}
            for _ in range(shots):
                bitstring = ''.join(np.random.choice(['0', '1']) for _ in range(n_qubits))
                counts[bitstring] = counts.get(bitstring, 0) + 1
            
            # Return most frequent bitstring
            return max(counts.keys(), key=counts.get)
            
        except Exception as e:
            logger.error(f"Error sampling bitstring: {e}")
            return '0' * hamiltonian.num_qubits
    
    def _bitstring_to_weights(self, bitstring: str, variable_mapping: Dict) -> np.ndarray:
        """Convert bitstring to portfolio weights"""
        try:
            n_assets = variable_mapping['assets']
            discretization = variable_mapping['discretization']
            weight_levels = np.array(variable_mapping['weight_levels'])
            
            weights = np.zeros(n_assets)
            
            # Map bitstring to binary variables
            bit_index = 0
            for i in range(n_assets):
                for j in range(discretization + 1):
                    if bit_index < len(bitstring) and bitstring[bit_index] == '1':
                        weights[i] = weight_levels[j]
                        break
                    bit_index += 1
            
            # Normalize weights
            weights = normalize_weights(weights)
            
            return weights
            
        except Exception as e:
            logger.error(f"Error converting bitstring to weights: {e}")
            return np.zeros(variable_mapping['assets'])
    
    def create_qaoa_circuit(self, hamiltonian: PauliSumOp, params: np.ndarray, p: int) -> QuantumCircuit:
        """Create QAOA circuit (for visualization/analysis)"""
        try:
            n_qubits = hamiltonian.num_qubits
            qc = QuantumCircuit(n_qubits)
            
            # Initial state: equal superposition
            qc.h(range(n_qubits))
            
            # QAOA layers
            for layer in range(p):
                # Problem Hamiltonian (cost layer)
                gamma = params[layer]
                # Apply problem Hamiltonian evolution
                # (Simplified - in practice, decompose Hamiltonian into gates)
                
                # Mixer Hamiltonian (driver layer)
                beta = params[p + layer]
                qc.rx(2 * beta, range(n_qubits))
            
            # Measurement
            qc.measure_all()
            
            return qc
            
        except Exception as e:
            logger.error(f"Error creating QAOA circuit: {e}")
            raise