from pl import parser
import nodes
from nodes import draw_nodes
from transforms import * 
from validity import * 

data = '(p ^ ~p) | (q | ~ q) | (a -> b -> c)'
data = '(a ^ b) | (c ^ d)'
data = 'r -> (s -> (t ^ s -> r))'
data = '~p ^ q -> p ^ (r -> q)'
# data = '(p|q|r) ^ ((p|~q) ^ ((q|~r) ^ ((r|~p) ^ (~p|~q|~r))))'
data = '(p|q|r) ^ (p|~q) ^ (q|~r) ^ (r|~p) ^ (~p|~q|~r)'
data = 'p^~(q|~p)'

parse_tree = parser.parse(data)
print(parse_tree)

def is_satisfiable(root : Node) : 
    temp = CNF(Not_node(root))
    return not is_CNF_valid(temp)


print(is_satisfiable(parse_tree))
