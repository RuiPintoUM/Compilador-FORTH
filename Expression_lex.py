import ply.lex as lex

literals=['(',')','=','!']
tokens=( 
    #'OPREL',
    'NUM',   
    'OPAD',     
    'OPSUB',      
    'OPMUL', 
    'OPDIV',  
    'OPMOD',
    'ID',
    'STRING',
    'PRINT',  
    'CHAR',
    'VARIABLE',
    'DO',
    'LOOP', 
    'EMIT', 
    'SPACE',
    'CR',
    'KEY',
    'DUP',
    'STARTDEF',
    'FINISHDEF'
)

t_OPAD=r'\+' 
t_OPSUB = r'\-'
t_OPMUL=r'\*'
t_OPDIV=r'\/'
t_OPMOD=r'\%'
t_STARTDEF=r'\:'
t_FINISHDEF=r'\;'

def t_NUM(t):
    r'\d+'
    return t

def t_CHAR(t):
    r'CHAR'
    return t

def t_EMIT(t):
    r'EMIT'
    return t

def t_SPACE(t):
    r'SPACE'
    return t

def t_CR(t):
    r'CR'
    return t

def t_KEY(t):
    r'KEY'
    return t

def t_DUP(t):
    r'DUP'
    return t

def t_PRINT(t):
    r'\.'
    return t

def t_VARIABLE(t):
    r'VARIABLE'
    return t

def t_DO(t):
    r'DO'
    return t

def t_LOOP(t):
    r'LOOP'
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

def t_ID(t):
    r'[a-zA-z][^\s!+*-/%:;]*'
    return t

def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)

t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()
