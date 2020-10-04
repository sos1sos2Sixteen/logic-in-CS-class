from abc import ABC, abstractmethod, abstractproperty
from graphviz import Digraph

class Uid_dispatcher(object) : 

    def __init__(self) : 
        self.counter = -1

    @property
    def uid(self) : 
        self.counter += 1
        return f'n{self.counter}'

_UID_DISPATHCER = Uid_dispatcher()

class Node(ABC) : 
    uid : int 
    @abstractmethod
    def draw_graph(self, dot : Digraph) : 
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def clone(self) -> "Node" : 
        pass

class Atom_node(Node) : 
    def __init__(self, v) : 
        self.uid = _UID_DISPATHCER.uid
        self.value = v

    def draw_graph(self, dot: Digraph):
        dot.node(self.uid, f'{self.value}', shape='box', style='filled')
        return self.uid

    def __repr__(self) -> str:
        return f'{self.value}'

    def clone(self) -> "Node":
        return Atom_node(self.value)

class Not_node(Node) : 
    def __init__(self, child : Node) -> None:
        self.uid = _UID_DISPATHCER.uid
        self.child = child 

    def draw_graph(self, dot: Digraph):
        dot.node(self.uid, '~', shape='circle')
        child_id = self.child.draw_graph(dot)
        dot.edge(self.uid, child_id)
        return self.uid

    def __repr__(self) -> str:
        if not isinstance(self.child, (Not_node, Atom_node)) : 
            return f'~({self.child})'
        else : 
            return f'~{self.child}'

    def clone(self) -> "Node":
        return Not_node(self.child.clone())

class Conjunctive_node(Node) : 
    def __init__(self, left : Node, right : Node) -> None:
        self.uid = _UID_DISPATHCER.uid
        self.left = left 
        self.right = right 

    def draw_graph(self, dot: Digraph):
        dot.node(self.uid, '^', shape='circle')
        left_id = self.left.draw_graph(dot)
        right_id = self.right.draw_graph(dot)
        dot.edges([
            (self.uid, left_id),
            (self.uid, right_id)
        ])
        return self.uid

    def __repr__(self) -> str:
        return f'({self.left} ^ {self.right})'

    def clone(self) -> "Node":
        return Conjunctive_node(
            self.left.clone(),
            self.right.clone()
        )

class Disjunctive_node(Node) : 
    def __init__(self, left : Node, right:Node) -> None:
        self.uid = _UID_DISPATHCER.uid
        self.left = left
        self.right = right

    def draw_graph(self, dot: Digraph):
        dot.node(self.uid, '|', shape='circle')
        left_id = self.left.draw_graph(dot)
        right_id = self.right.draw_graph(dot)
        dot.edges([
            (self.uid, left_id),
            (self.uid, right_id)
        ])
        return self.uid

    def __repr__(self) -> str:
        return f'({self.left} | {self.right})'

    def clone(self) -> "Node":
        return Disjunctive_node(
            self.left.clone(),
            self.right.clone()
        )

class Implication_node(Node) : 
    def __init__(self, left : Node, right:Node) -> None:
        self.uid = _UID_DISPATHCER.uid
        self.left = left
        self.right = right

    def draw_graph(self, dot: Digraph):
        dot.node(self.uid, '->', shape='circle')
        left_id = self.left.draw_graph(dot)
        right_id = self.right.draw_graph(dot)
        dot.edges([
            (self.uid, left_id),
            (self.uid, right_id)
        ])
        return self.uid

    def __repr__(self) -> str:
        return f'({self.left} -> {self.right})'

    
    def clone(self) -> "Node":
        return Disjunctive_node(
            self.left.clone(),
            self.right.clone()
        )
    

def draw_nodes(root : Node) : 
    dot = Digraph(comment='parse tree')
    root.draw_graph(dot)
    dot.view(cleanup=True)