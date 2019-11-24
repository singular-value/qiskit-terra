# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit import *

from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CommutationAnalysis, CommutativeCancellation, MatchZZInteraction#, CommutativeMatchZZInteraction

circuit = QuantumCircuit(4)
# Quantum Instantaneous Polynomial Time example
circuit.cx(0, 1)
circuit.z(1)
circuit.cx(0, 1)
circuit.cx(0, 2)
circuit.rz(0.5, 2)
circuit.rz(0.3, 0)
circuit.cx(0, 3)
circuit.cx(0, 2)

print(circuit)

pm = PassManager()
pm.append([CommutationAnalysis(), MatchZZInteraction()])
new_circuit=pm.run(circuit)
print(new_circuit)
