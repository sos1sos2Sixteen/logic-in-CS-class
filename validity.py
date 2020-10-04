from nodes import * 
def _recur_is_valid_disjunct(root : Node, literals) -> bool : 

    if isinstance(root, Atom_node) : 
        id = root.value
        if f'~{id}' in literals : 
            return True
        elif id not in literals : 
            literals.add(id)
        return False
    elif isinstance(root, Not_node) : 
        id = root.child.value
        neg = f'~{id}'
        if f'{id}' in literals : 
            return True
        elif neg not in literals : 
            literals.add(neg)
        return False
    elif isinstance(root, (Conjunctive_node, Disjunctive_node)) : 
        res = False
        res = res or _recur_is_valid_disjunct(root.left, literals)
        if res : 
            return True
        res = res or _recur_is_valid_disjunct(root.right, literals)
        return res


    
def is_valid_disjunct(root : Node) -> bool : 
    literals = set()
    return _recur_is_valid_disjunct(root, literals)


def is_CNF_valid(root : Node) -> bool : 
    """root should be in CNF"""

    if isinstance(root, (Atom_node, Not_node)) : 
        return False
    elif isinstance(root, Conjunctive_node) : 
        return is_CNF_valid(root.left) and is_CNF_valid(root.right)
    elif isinstance(root, Disjunctive_node) : 
        return is_valid_disjunct(root)
