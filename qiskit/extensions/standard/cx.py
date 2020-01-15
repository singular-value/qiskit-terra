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

from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.direct_rx import DirectRXGate
from qiskit.extensions.standard.cr import CRGate


class CnotGate(Gate):
    """controlled-NOT gate."""

    def __init__(self):
        """Create new CNOT gate."""
        super().__init__("cx", 2, [])

    def _define(self):
        from qiskit import PULSE_BACKED_OPTIMIZATION
        if PULSE_BACKED_OPTIMIZATION:
            """
            Cnot decomposes into:
            ---RX(pi)---Sdag---| CR with X side effect |----
            --RX(pi/2)---------|          pi/2         |----
            algassert.com/quirk#circuit=%7B%22cols%22%3A%5B%5B%22X%22%2C%7B%22id%22%3A%22Rxft%22%2C%22
            arg%22%3A%22pi%2F2%22%7D%5D%2C%5B%22Z%5E-%C2%BD%22%5D%2C%5B%22%E2%97%A6%22%2C%7B%22id%22%3A
            %22Rxft%22%2C%22arg%22%3A%22pi%2F4%22%7D%5D%2C%5B%22%E2%80%A2%22%2C%7B%22id%22%3A%22Rxft%22
            %2C%22arg%22%3A%22-pi%2F4%22%7D%5D%2C%5B%5D%2C%5B%22X%22%5D%2C%5B%22%E2%97%A6%22%2C%7B%22id
            %22%3A%22Rxft%22%2C%22arg%22%3A%22-pi%2F4%22%7D%5D%2C%5B%5D%2C%5B%22%E2%80%A2%22%2C%7B%22id
            %22%3A%22Rxft%22%2C%22arg%22%3A%22pi%2F4%22%7D%5D%5D%7D
            """
            definition = []
            q = QuantumRegister(2, "q")
            rule = [
                (U1Gate(pi/2), [q[0]], []),
                (DirectRXGate(pi), [q[0]], []),
                (DirectRXGate(pi/2), [q[1]], []),
                (CRGate(pi/2), [q[0], q[1]], []),
            ]
            for inst in rule:
                definition.append(inst)
            self.definition = definition
        else:
            super()._define()

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
