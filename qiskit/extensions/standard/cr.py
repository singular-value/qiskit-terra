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
Cross-Resonance gate.
"""
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister


class CRGate(Gate):
    """Cross-Resonance gate."""

    def __init__(self, theta):
        super().__init__("cr", 2, [theta])

    def inverse(self):
        """Invert this gate."""
        return CRGate(-self.params[0])


def cr(self, theta, ctl, tgt):
    """Apply cross-resonance from ctl to tgt with angle theta."""
    return self.append(CRGate(theta), [ctl, tgt], [])


QuantumCircuit.cr = cr
