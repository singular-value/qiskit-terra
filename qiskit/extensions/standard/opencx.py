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
open-controlled-NOT gate.
"""

import numpy

from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.direct_rx import DirectRXGate
from qiskit.extensions.standard.cr import CRGate


class OpenCnotGate(Gate):
    """open-controlled-NOT gate."""

    def __init__(self):
        """Create new open-CNOT gate."""
        super().__init__("open_cx", 2, [])

    def _define(self):
        """
        Open Cnot decomposes into:
        ------Sdag---| CR with X side effect |--RX(pi)---
        --RX(pi/2)---|          pi/2         |-----------
        """
        definition = []
        q = QuantumRegister(2, "q")
        rule = [
            (U1Gate(-pi/2), [q[0]], []),
            (DirectRXGate(pi/2), [q[1]], []),
            (CRGate(pi/2), [q[0], q[1]], []),
            (DirectRXGate(pi), [q[0]], []),
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate."""
        return OpenCnotGate()  # self-inverse

    def to_matrix(self):
        """Return a Numpy.array for the Open Cx gate."""
        return numpy.array([[0, 1, 0, 0],
                            [1, 0, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]], dtype=complex)


def open_cx(self, ctl, tgt):
    """Apply open CX from ctl to tgt."""
    return self.append(OpenCnotGate(), [ctl, tgt], [])


QuantumCircuit.open_cx = open_cx
QuantumCircuit.open_cnot = open_cx
