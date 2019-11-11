# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
controlled-NOT gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.direct_rx import DirectRXGate
from qiskit.extensions.standard.cr import CRGate


class CnotGate(ControlledGate):
    """controlled-NOT gate."""

    def __init__(self):
        """Create new CNOT gate."""
        super().__init__("cx", 2, [], num_ctrl_qubits=1)
        self.base_gate = XGate
        self.base_gate_name = "x"

    def _define(self):
        """
        Cnot decomposes into:
        ---RX(pi)---| CR |--RX(pi)--|  CR |--
        --RX(pi/2)--|pi/4|----------|-pi/4|--
        algassert.com/quirk#circuit=%7B%22cols%22%3A%5B%5B%22X%22%2C%22X%5E%C2%BD%22%5D%2C%5B%22%E2%
        97%A6%22%2C%22X%5E%C2%BC%22%5D%2C%5B%22%E2%80%A2%22%2C%22X%5E-%C2%BC%22%5D%2C%5B%22X%22%5D%2
        C%5B%22%E2%97%A6%22%2C%22X%5E-%C2%BC%22%5D%2C%5B%22%E2%80%A2%22%2C%22X%5E%C2%BC%22%5D%5D%7D
        """
        definition = []
        q = QuantumRegister(2, "q")
        rule = [
            (DirectRXGate(pi), [q[0]], []),
            (DirectRXGate(pi/2), [q[1]], []),
            (CRGate(pi/4), [q[0], q[1]], []),
            (DirectRXGate(pi), [q[0]], []),
            (CRGate(-pi/4), [q[0], q[1]], []),
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate."""
        return CnotGate()  # self-inverse

    def to_matrix(self):
        """Return a Numpy.array for the Cx gate."""
        return numpy.array([[1, 0, 0, 0],
                            [0, 0, 0, 1],
                            [0, 0, 1, 0],
                            [0, 1, 0, 0]], dtype=complex)


def cx(self, ctl, tgt):  # pylint: disable=invalid-name
    """Apply CX from ctl to tgt."""
    return self.append(CnotGate(), [ctl, tgt], [])


QuantumCircuit.cx = cx
QuantumCircuit.cnot = cx
