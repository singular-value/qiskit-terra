"""Match cx(c,t) rz(t) cx(c,t) sequences and convert to ZZInteractionGate."""
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.extensions.standard.direct_rx import DirectRXGate
from qiskit.dagcircuit.dagnode import DAGNode
import numpy as np
class CommutativeMatchZZInteraction(TransformationPass):
    def run(self, dag):
        """Run the MatchZZInteraction pass on `dag`.
        Args:
            dag (DAGCircuit): the directed acyclic graph to run on.
        Returns:
            DAGCircuit: Transformed DAG.
        """

        for wire in dag.wires:
            wire_name = "{0}[{1}]".format(str(wire.register.name), str(wire.index))
            wire_commutation_set = self.property_set['commutation_set'][wire_name]

            for com_set_idx, com_set in enumerate(wire_commutation_set):
                if com_set_idx == len(wire_commutation_set) - 2:
                    break
                if com_set == []:
                    continue
                for node in com_set:
                    if (node.name == 'cx' and 
                        node.qargs[1] == wire):
                                
                        next_com_set = wire_commutation_set[com_set_idx+1]

                        for next_node in next_com_set:
                            if(node.name == 'rz' or node.name == 'z'):
                                nn_com_set = wire_commutation_set[com_set_idx+1]
                                for nn_node in next_com_set:
                                    if (node.name == 'cx' and node.qargs[1] == wire):

                                        if suc_node.name == 'z':
                                            new_op = ZZInteractionGate(np.pi)
                                        else:
                                            new_op = ZZInteractionGate(suc_node.op.params[0])
                                        new_node = DAGNode({'type': 'op',
                                                            'op': new_op,
                                                            'name': 'cz',
                                                            'qargs': node.qargs
                                                            })
                                        dag.substitute_node(node, new_op, inplace=True)

                                        dag.remove_op_node(next_node)
                                        dag.remove_op_node(nn_node)

        return dag
