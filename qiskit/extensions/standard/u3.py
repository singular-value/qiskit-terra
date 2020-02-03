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
Two-pulse single-qubit gate.
"""

import numpy as np
from qiskit import PulseBackedOptimizationContext
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit, QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.direct_rx import DirectRXGate


class U3Gate(Gate):
    """Two-pulse single-qubit gate."""

    def __init__(self, theta, phi, lam, label=None):
        """Create new two-pulse single qubit gate."""
        super().__init__("u3", 1, [theta, phi, lam], label=label)

    def _define(self):
        if PulseBackedOptimizationContext.get():
            """Decompose via identity similar to [McKay et al. 2017, 17] (arxiv.org/pdf/1612.00858.pdf).
            U3(theta, phi, lambda) = RZ(lambda - pi/2) * RX(theta) * RZ(phi + pi/2)
            """
            definition = []
            q = QuantumRegister(1, "q")
            theta, phi, lam = self.params[0], self.params[1], self.params[2]
            rule = [
                (U1Gate(lam - np.pi/2), [q[0]], []),
                (DirectRXGate(theta), [q[0]], []),
                (U1Gate(phi + np.pi/2), [q[0]], []),
            ]
            for inst in rule:
                definition.append(inst)
            self.definition = definition
        else:
            super()._define()

    def inverse(self):
        """Invert this gate.

        u3(theta, phi, lamb)^dagger = u3(-theta, -lam, -phi)
        """
        return U3Gate(-self.params[0], -self.params[2], -self.params[1])

    def to_matrix(self):
        """Return a Numpy.array for the U3 gate."""
        theta, phi, lam = self.params
        theta, phi, lam = float(theta), float(phi), float(lam)
        return np.array(
            [[
                np.cos(theta / 2),
                -np.exp(1j * lam) * np.sin(theta / 2)
            ],
             [
                 np.exp(1j * phi) * np.sin(theta / 2),
                 np.exp(1j * (phi + lam)) * np.cos(theta / 2)
             ]],
            dtype=complex)


def u3(self, theta, phi, lam, q):  # pylint: disable=invalid-name
    """Apply u3 to q."""
    return self.append(U3Gate(theta, phi, lam), [q], [])


QuantumCircuit.u3 = u3
