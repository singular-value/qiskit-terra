"""Match cx(c,t) rz(t) cx(c,t) sequences and convert to ZZInteractionGate."""
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.extensions.standard.direct_rx import DirectRXGate
from qiskit.extensions.standard.zz_interaction import ZZInteractionGate
from qiskit.dagcircuit.dagnode import DAGNode
import numpy as np

class MatchZZInteraction(TransformationPass):
    def run(self, dag):
        """Run the MatchZZInteraction pass on `dag`.
        Args:
            dag (DAGCircuit): the directed acyclic graph to run on.
        Returns:
            DAGCircuit: Transformed DAG.
        """

        matched = [] 
        to_remove = []
        for node in dag.topological_op_nodes():
            if node in matched:
                continue

            if node.type == 'op' and  node.name == 'cx':
                for suc_node in dag.successors(node):
                    if (suc_node.type == 'op' and
                        (suc_node.name == 'z' or
                         suc_node.name == 'rz') and
                        suc_node.qargs[0] == node.qargs[1]):

                        for sucsuc_node in dag.successors(suc_node):

                            if (sucsuc_node.type == 'op' and
                                sucsuc_node.name == 'cx' and
                                sucsuc_node.qargs == node.qargs):
                                matched = matched + [node, suc_node, sucsuc_node]
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
                                to_remove = to_remove + [suc_node, sucsuc_node]             



        for node in to_remove:
            dag.remove_op_node(node)


        return dag
