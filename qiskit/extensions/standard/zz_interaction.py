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
ZZ-Interaction (e^{-i ZZ theta}) gate.
"""
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.cx import CnotGate


class ZZInteractionGate(Gate):
    """ZZ-Interaction (e^{-i ZZ theta}) gate."""

    def __init__(self, theta):
        super().__init__("zz_interaction", 2, [theta])

    def _define(self):
        """
        TODO(pranav): decompose to a single CR gate
        """
        definition = []
        q = QuantumRegister(2, "q")
        rule = [
            (CnotGate(), [q[0], q[1]], []),
            (U1Gate(self.params[0]), [q[1]], []),
            (CnotGate(), [q[0], q[1]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition


def zz_interaction(self, theta, q1, q2):
    return self.append(ZZInteractionGate(theta), [q1, q2], [])


QuantumCircuit.zz_interaction = zz_interaction
