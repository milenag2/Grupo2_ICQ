import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import MCXGate

def run_grover_simulation(n_qubits):
    try:
        print(f"Attempting simulation for n = {n_qubits} qubits...")

        if n_qubits <= 0:
            print(f"Skipping simulation for n = {n_qubits} qubits as it's not a valid quantum circuit size.")
            return False

        grover_circuit = QuantumCircuit(n_qubits, n_qubits)

        # Inicialização com Hadamards
        def initialize_s(qc, qubits):
            for q in qubits:
                qc.h(q)
            return qc

        grover_circuit = initialize_s(grover_circuit, range(n_qubits))

        # Oracle: marca o estado |11...11⟩ (todos os qubits em 1)
        # This is a phase oracle that applies a -1 phase to the state |1...1>
        if n_qubits == 1:
            grover_circuit.z(0) # For 1 qubit, marking |1> is a Z gate
        else:
            # Implement multi-controlled Z using H and MCXGate
            control_qubits = list(range(n_qubits - 1))
            target_qubit = n_qubits - 1
            grover_circuit.h(target_qubit)
            grover_circuit.append(MCXGate(n_qubits - 1), control_qubits + [target_qubit])
            grover_circuit.h(target_qubit)

        # Difusão (inversão sobre a média)
        grover_circuit.h(range(n_qubits))
        grover_circuit.x(range(n_qubits))

        # Apply multi-controlled Z for diffusion
        if n_qubits == 1:
            grover_circuit.z(0) # For 1 qubit, diffusion is also a Z gate
        else:
            control_qubits_diffusion = list(range(n_qubits - 1))
            target_qubit_diffusion = n_qubits - 1
            grover_circuit.h(target_qubit_diffusion)
            grover_circuit.append(MCXGate(n_qubits - 1), control_qubits_diffusion + [target_qubit_diffusion])
            grover_circuit.h(target_qubit_diffusion)

        grover_circuit.x(range(n_qubits))
        grover_circuit.h(range(n_qubits))

        # Medidas
        grover_circuit.measure(range(n_qubits), range(n_qubits))

        # Simular o circuito
        simulator = Aer.get_backend('qasm_simulator')
        compiled_circuit = transpile(grover_circuit, simulator)
        job = simulator.run(compiled_circuit, shots=1024)
        result = job.result()
        counts = result.get_counts(grover_circuit)

        # Plotar o histograma (opcional, pode ser muito grande para n grande)
        # plot_histogram(counts)
        # plt.savefig(f'grover_histogram_{n_qubits}_qubits.png')

        print(f"Simulation successful for n = {n_qubits} qubits.")
        return True

    except Exception as e:
        print(f"Simulation failed for n = {n_qubits} qubits. Error: {e}")
        return False

# Loop para encontrar o limite de qubits
max_qubits_supported = 0
# Start from 1 qubit, test up to a reasonable limit (e.g., 25-30 qubits for Aer simulator)
# The exact limit depends on available memory and simulator capabilities.
for n in range(1, 30):
    if run_grover_simulation(n):
        max_qubits_supported = n
    else:
        print(f"The code stopped running at n = {n} qubits.")
        break

print(f"The maximum number of qubits supported by this code is: {max_qubits_supported}")


