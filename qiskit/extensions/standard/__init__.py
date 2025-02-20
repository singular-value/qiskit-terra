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

"""Standard gates."""
from .barrier import Barrier
from .direct_rx import DirectRXGate
from .ccx import ToffoliGate
from .cr import CRGate
from .cswap import FredkinGate
from .cx import CnotGate
from .cy import CyGate
from .cz import CzGate
from .swap import SwapGate
from .h import HGate
from .iden import IdGate
from .s import SGate
from .s import SdgGate
from .t import TGate
from .t import TdgGate
from .u1 import U1Gate
from .u2 import U2Gate
from .u3 import U3Gate
from .x import XGate
from .y import YGate
from .z import ZGate
from .r import RGate
from .rx import RXGate
from .ry import RYGate
from .rz import RZGate
from .cu1 import Cu1Gate
from .ch import CHGate
from .crz import CrzGate
from .cu3 import Cu3Gate
from .rzz import RZZGate
from .rxx import RXXGate
from .ms import MSGate
from .zz_interaction import ZZInteractionGate
