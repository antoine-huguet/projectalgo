

def block_to_string(Block):
    translation = {'IF_BLOCK':('if ',':'),
    'ELSE_BLOCK':('else:'),
    'END_BLOCK':('',''),
    'WHILE_BLOCK':('while ',':'),
    'MINUS_BLOCK':('-',''),
    'PLUS_BLOCK':('+',''),
    'PL_BLOCK':('(',''),
    'PR_BLOCK':(')',''),
    'DIV_BLOCK':('/',''),
    'X_BLOCK':('*',''),
    'EQUAL_BLOCK':('==',''),
    'DIF_BLOCK':('-',''),
    'SUPL_BLOCK':('>=',''),
    'SUP_BLOCK':('>',''),
    'INFL_BLOCK':('<=',''),
    'INF_BLOCK':('<',''),
    'A_BLOCK':('a',''),
    'B_BLOCK':('b',''),
    'C_BLOCK':('c',''),
    'D_BLOCK':('d',''),
    'E_BLOCK':('e',''),
    'F_BLOCK':('f',''),
    'AFFECTATION_BLOCK':'=',
    'PRINT_BLOCK':('print(',')')
    }
    name = type(Block).__name__
    if name=='INPUT_BLOCK':
        return (Block.text,'')
    return translation[name]

def listBlock_to_code(L):
    res=''
    t=0
    for line in L[1:]:
        row =''
        if not line:
            pass
        elif type(line[0]).__name__=='END_BLOCK':
            t -= 1
            continue
        else:
            pre,post = block_to_string(line[0])
            row+= t*'    ' + pre
            for block in line[1:]:
                row+=block_to_string(block)[0]
            row+=post
            if type(line[0]).__name__=='IF_BLOCK' or type(line[0]).__name__=='WHILE_BLOCK':
                t+=1
        res+= row + '\n'
    return res
