import ply.yacc as yacc
import sys

from Expression_lex import tokens

def p_Prog(p):
    """
    Prog : Frase
    """
    p[0] = 'pushn ' + str(parser.next_add) +'\n'
    p[0] += 'start\n'
    p[0] += p[1]
    p[0] += 'stop\n'

def p_Frase1(p):
    """
    Frase : Frase ExpRel
    """
    p[0] = p[1] + p[2] 
    #print(p[0])
    #print("Frase1")

def p_Frase2(p):
    """
    Frase :
    """
    p[0] = ''
    #print("Frase2")

def p_Frase3(p):
    """
    Frase : FuncDef
    """
    p[0] = p[1]
    #print("Frase3")

def p_ExpRel1(p):
    """
    ExpRel : Exp
    """
    p[0]=p[1]
    #print("ExpRel1")  
    
def p_ExpRel2(p):
    """
    ExpRel : PRINT
    """
    p[0] = 'WRITEI\n'
    
def p_ExpRel3(p):
    """
    ExpRel : EMIT
    """
    p[0] = 'WRITECHR\n'

def p_ExpRel4(p):
    """
    ExpRel : SPACE
    """
    p[0] = 'pushs " "\n' + 'WRITES\n'

def p_ExpRel5(p):
    """
    ExpRel : CR
    """
    p[0] = 'WRITELN\n'    

def p_ExpRel6(p):
    """
    ExpRel : KEY
    """
    p[0] = 'READ\n' 

def p_ExpRel7(p):
    """
    ExpRel : DUP
    """
    p[0] = 'DUP 1\n'       

def p_ExpRel8(p):
    """
    ExpRel : AtribDecl
    """
    p[0]=p[1]
    #print("ExpRel1")

def p_ExpRel9(p):
    """
    ExpRel : Atrib
    """
    p[0] = p[1]

def p_ExpRel10(p):
    """
    ExpRel : ExpStr
    """
    p[0]=p[1]
    #print("ExpRel1")

def p_ExpRel11(p):
    """
    ExpRel : PRINT STRING
    """
    p[0] = 'pushs ' + p[2] + '\nWRITES\n'
    #print("ExpRel1")

def p_ExpRel12(p):
    """
    ExpRel : LoopDef
    """
    p[0] = p[1]

def p_AtribDecl(p):
    """
    AtribDecl : VARIABLE ID
    """
    if p[2] not in parser.tab_id:
        parser.tab_id[p[2]] = parser.next_add
        parser.next_add += 1
        p[0] = ''  # Nenhuma instrução de máquina é necessária apenas para declarar
    else:
        print(f"Erro: Variável {p[2]} já declarada.")
        p[0] = ''
        parser.exito = False

def p_Atrib(p):
    """
    Atrib : Exp ID '!'
    """
    if p[2] in parser.tab_id.keys(): 
        p[0] = p[1] + 'storeg ' + str(parser.tab_id[p[2]]) + '\n'
    else:
        print(f"Variável {p[2]} não declarada")
        p[0] = ''
        parser.exito = False

def p_Exp1(p):
    """
    Exp : Exp Exp OPAD
    """
    p[0] = p[1] + p[2] + 'ADD\n'
    
def p_Exp2(p):
    """
    Exp : Exp Exp OPSUB
    """
    p[0] = p[1] + p[2] + 'SUB\n'
    

def p_Exp3(p):
    """
    Exp : Exp Exp OPMUL
    """
    p[0] = p[1] + p[2] + 'MUL\n'
    
def p_Exp4(p):
    """
    Exp : Exp Exp OPDIV
    """
    if p[2].strip() == 'pushi 0':  # Verifica se é zero 
        print("Erro: Divisão por zero.")
        p[0] = ''
        parser.exito = False
    else:
        p[0] = p[1] + p[2] + 'DIV\n'
    

def p_Exp5(p):
    """
    Exp : Exp Exp OPMOD
    """
    p[0] = p[1] + p[2] + 'MOD\n'

def p_Exp6(p):
    """
    Exp : NUM
    """
    p[0] = 'pushi ' + p[1] + '\n'

def p_Exp7(p):
    """
    Exp : ID
    """
    if p[1] in parser.function_defs:
        p[0] = parser.function_defs[p[1]]
    elif p[1] in parser.tab_id.keys(): 
        p[0] = 'pushg ' + str(parser.tab_id[p[1]]) + '\n'
    else:
        print("Erro Semantico")
        p[0] = ''
        parser.exito = False
    
def p_Exp8(p):
    '''
    Exp : Exp Exp
    '''
    p[0] = p[1] + p[2]

def p_ExpStr1(p):
    '''
    ExpStr : CHAR ID
           | CHAR '!'
           | CHAR OPAD
           | CHAR OPSUB
           | CHAR OPMUL
           | CHAR OPDIV
           | CHAR OPMOD
           | CHAR STARTDEF
           | CHAR FINISHDEF
    '''
    p[0] = 'pushs "' + p[2] + '"\nCHRCODE\n'

def p_FuncDef(p):
    """
    FuncDef : STARTDEF ID Frase FINISHDEF
    """
    if p[2] in parser.function_defs:
        print(f"Erro: Função {p[2]} já declarada.")
        p[0] = ''
        parser.exito = False
    else:
        # Salva a definição da função no dicionário
        parser.function_defs[p[2]] = p[3]
        parser.next_add += 1
        p[0] = '' 

def p_FuncDef2(p):
    """
    FuncDef : FuncDef FuncDef
    """
    p[0] = p[1] + p[2]
 

def p_LoopDef(p):
    """
    LoopDef : Exp Exp DO Frase LOOP
    """

    if(p[1] < p[2]):
        print("ERRO! O ciclo não pode ter um valor inicial maior que o valor final")
        parser.exito = False

    parser.tab_id['_aux'] = parser.next_add
    parser.next_add += 1
    
    current_loop = parser.next_loop
    
    p[0] = p[1] + p[2] + 'SUB\n'
    p[0] += 'storeg ' + str(parser.tab_id['_aux']) + '\n'
    p[0] += 'WHILE ' + str(current_loop) + ':\n'
    p[0] += 'pushg ' + str(parser.tab_id['_aux']) + '\n'
    p[0] += 'pushi 0\n'
    p[0] += 'SUP\njz ENDWHILE' + str(current_loop) + '\n'
    p[0] += p[4]
    p[0] += 'pushg ' + str(parser.tab_id['_aux']) + '\n'
    p[0] += 'pushi 1\n'
    p[0] += 'SUB\n'
    p[0] += 'storeg ' + str(parser.tab_id['_aux']) + '\n'
    p[0] += 'JUMP WHILE' + str(current_loop) + '\n'
    p[0] += 'ENDWHILE' + str(current_loop) + ':\n'
    parser.next_loop += 1
    


def p_error(p):
    print("Erro Sintático! Reescreva a frase")
    parser.exito = False

parser = yacc.yacc()
parser.exito = True
parser.tab_id = {}
parser.function_defs = {}
parser.next_add = 0
parser.next_loop = 0

fonte = ""
for linha in sys.stdin:
    fonte += linha


codigo = parser.parse(fonte)

if parser.exito:
    print("Parsing teminou com sucesso!")
    print(codigo)
