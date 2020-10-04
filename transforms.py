
from nodes import *
from typing import Dict

def implication_elimination(root : Node) -> Node : 
    if isinstance(root, Atom_node) : 
        return Atom_node(root.value)
    elif isinstance(root, Not_node) : 
        return Not_node(implication_elimination(root.child))
    elif isinstance(root, Conjunctive_node) : 
        return Conjunctive_node(
            implication_elimination(root.left),
            implication_elimination(root.right)
        )
    elif isinstance(root, Disjunctive_node) : 
        return Disjunctive_node(
            implication_elimination(root.left),
            implication_elimination(root.right)
        )
    elif isinstance(root, Implication_node) :
        # rewrite : (p -> q) => (~p | q)
        return Disjunctive_node(
            Not_node(implication_elimination(root.left)),
            implication_elimination(root.right)
        )

def disjunction_distribution(phi1 : Node, phi2 : Node) -> Node : 
    # suppose phi1 and phi2 are in CNF
    if isinstance(phi1, Conjunctive_node) : 
        eta1, eta2 = phi1.left, phi1.right
        return Conjunctive_node(
            disjunction_distribution(eta1, phi2),
            disjunction_distribution(eta2, phi2)
        )
    elif isinstance(phi2, Conjunctive_node) : 
        eta1, eta2 = phi2.left, phi2.right
        return Conjunctive_node(
            disjunction_distribution(phi1, eta1),
            disjunction_distribution(phi1, eta2)
        )
    else : 
        return Disjunctive_node(phi1.clone(), phi2.clone())


def NNF(root : Node) -> Node : 
    if isinstance(root, Atom_node) : 
        return root.clone()
    elif isinstance(root, Conjunctive_node) : 
        return Conjunctive_node(NNF(root.left), NNF(root.right))
    elif isinstance(root, Disjunctive_node) : 
        return Disjunctive_node(NNF(root.left), NNF(root.right))
    elif isinstance(root, Not_node) : # begin with ~
        phi = root.child
        if isinstance(phi, Atom_node) : # negation literal
            return root.clone()
        elif isinstance(phi, Not_node) : # double negation
            return phi.child.clone()
        elif isinstance(phi, Conjunctive_node) : # de morgan : ~(a^b) => (~a | ~b)
            a, b = phi.left, phi.right
            return Disjunctive_node(NNF(Not_node(a)), NNF(Not_node(b)))
        elif isinstance(phi, Disjunctive_node) : # de morgan : ~(a|b) => (~a ^ ~b)
            a, b = phi.left, phi.right
            return Conjunctive_node(NNF(Not_node(a)), NNF(Not_node(b)))

def CNF(root : Node) -> Node : 
    root = implication_elimination(root)
    root = NNF(root)

    if isinstance(root, (Atom_node, Not_node)) : 
        # since root is in NNF, then a Not-node must imply Literal
        return root.clone()
    elif isinstance(root, Conjunctive_node) : 
        return Conjunctive_node(CNF(root.left), CNF(root.right))
    elif isinstance(root, Disjunctive_node) : 
        return disjunction_distribution(CNF(root.left), CNF(root.right))


def _recur_collect_DAG(root : Node, atoms : Dict[str, Node]) -> Node : 

    if isinstance(root, Atom_node) : 
        if root.value not in atoms : 
            atoms[root.value] = root.clone()
        return atoms[root.value]
    elif isinstance(root, Not_node) : 
        return Not_node(_recur_collect_DAG(root.child, atoms))
    elif isinstance(root, Conjunctive_node) : 
        return Conjunctive_node(
            _recur_collect_DAG(root.left, atoms),
            _recur_collect_DAG(root.right, atoms)
        )
    elif isinstance(root, Disjunctive_node) : 
        return Disjunctive_node(
            _recur_collect_DAG(root.left, atoms),
            _recur_collect_DAG(root.right, atoms)
        )
    elif isinstance(root, Implication_node) : 
        return Implication_node(
            _recur_collect_DAG(root.left, atoms),
            _recur_collect_DAG(root.right, atoms)
        )

def collect_DAG(root : Node) -> Node : 
    atoms = {}
    return _recur_collect_DAG(root, atoms), atoms
    
