import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

n = 3
grover_circuit = QuantumCircuit(n, n)

def initialize_s(qc, qubits):
    for q in qubits:
        qc.h(q)
    return qc

grover_circuit = initialize_s(grover_circuit, range(n))

# Oracle: marca |111⟩
grover_circuit.h(2)
grover_circuit.ccx(0, 1, 2)
grover_circuit.h(2)

# Difusão (inversão sobre a média) — versão correta
grover_circuit.h([0, 1, 2])
grover_circuit.x([0, 1, 2])
grover_circuit.h(2)
grover_circuit.ccx(0, 1, 2)
grover_circuit.h(2)
grover_circuit.x([0, 1, 2])
grover_circuit.h([0, 1, 2])


# Medida
grover_circuit.measure(range(n), range(n))


# Mostrar circuito
grover_circuit.draw('mpl')

# Simulação
simulator = Aer.get_backend('qasm_simulator')
compiled = transpile(grover_circuit, simulator)
job = simulator.run(compiled, shots=1024)
result = job.result()
counts = result.get_counts()

# Histograma
plot_histogram(counts)

