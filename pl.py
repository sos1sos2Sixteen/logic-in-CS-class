import ply.lex as lex 
import ply.yacc as yacc
from nodes import * 

tokens = (
    'ATOM',
    'NOT',
    'CONJUNCTION',  # ^  ->  ^
    'DISJUNCTION',  # V  ->  |
    'IMPLICATION',  # '->'
    'RPAREN',
    'LPAREN'
)

t_NOT = r'~'
t_CONJUNCTION = r'\^'
t_DISJUNCTION = r'\|'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_IMPLICATION = r'\->'
t_ATOM   = r'[a-zA-Z][a-zA-Z0-9]*'

def t_newline(t) : 
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t) : 
    print(f'Illegal character: {t.value[0]}')

lexer = lex.lex()

precedence = (
    ('right', 'IMPLICATION'),
    ('left', 'DISJUNCTION'),
    ('left', 'CONJUNCTION'),
    ('left', 'NOT')
)

def p_expression(p) : 
    """
    expression  : ATOM
                | NOT expression
                | LPAREN expression RPAREN
                | expression CONJUNCTION expression
                | expression DISJUNCTION expression
                | expression IMPLICATION expression
    """
    if len(p) == 2 : # number
        p[0] = Atom_node(p[1])
    elif len(p) == 3 : 
        p[0] = Not_node(p[2])
    elif p[1] == '(' : # (exp)
        p[0] = p[2]
    elif p[2] == '^' :  # exp1 ^ exp2
        p[0] = Conjunctive_node(p[1], p[3])
    elif p[2] == '|' : # exp1 | exp2
        p[0] = Disjunctive_node(p[1], p[3])
    else :  # exp1 -> exp2
        p[0] = Implication_node(p[1], p[3])

# Build the parser
parser = yacc.yacc()






