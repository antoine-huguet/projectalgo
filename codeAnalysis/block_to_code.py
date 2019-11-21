from Bloc import *
from Blocks import *


def code_executable(block_list):
    code=[]
    t=0
    for row in blocklist:
        for bloc in row:
            code.append(t*'\t')
            code.append(bloc.prefix)
            code.append(str(bloc.args[1]))
            code.append((bloc.condition().writeCondition()))
            code.append(bloc.suffix)
            t=t+bloc.tab
            code.append('\n')
    return(''.join(code))

def code_utilisateur(blocklist):
    code=['from time import sleep']
    L=[]
    t=0
    for row in blocklist:
        for bloc in row:
            code.append(t*'\t')
            code.append(bloc.prefix)
            if bloc.args[0]!=None:
                code.append(str(bloc.args[1]))
            code.append((bloc.condition().writeCondition()))
            code.append(bloc.suffix)
            #transcription d'une ligne dans l'ordre préfixe::condition::argument::suffixe
            t=t+bloc.tab
            if bloc.id==3 or bloc.id==4:
                L.append(bloc.args)
                code.append('\n time.sleep(.2) \n display(bloc.args)')
            #mise à jour de la liste des affectations et prints, pause et affichage
        code.append('\n')
    return(''.join(code),L)

def display(args):
    if args[0]==None:
        write_print(args[1])
    else:
        if args[1].uses_variables:
            string= str(args[0])+'='+args[1].text +'=' +str(evaluate.args[1])
        else:
            string= str(args[0])+'='+args[1].text
        write_affectation(string)



def graphic_to_model(blocklist):
    blocklist2=[]
    for row in blocklist:
        row2=[]
        for i in range(len(row)):
            if row[i].isinstance(IF_BLOCK):
                row2.append(Bloc(0,condition=Calculstring(row[i+1].text])))
            if row[i].isinstance(WHILE_BLOCK):
                row2.append(Bloc(1,condition=Calculstring(row[i+1].text])))
            if row[i].isinstance(AFFECTATION_BLOCK):
                row2.append(Bloc(3,args=[row2[i-1].prefix,Calculstring(row[i+1].text])))
            if row[i].isinstance(PRINT_BLOCK):
                row2.append(Bloc(2,args=[None,Calculstring(row[i+1].text)]))
            if row[i].isinstance(ELSE_BLOCK):
                row2.append(Bloc(4))
            if row[i].isinstance(END_BLOCK):
                row2.append(Bloc(5))
            if row[i].isinstance(A_BLOCK):
                row2.append(Bloc(6))
            if row[i].isinstance(B_BLOCK):
                row2.append(Bloc(7))
            if row[i].isinstance(C_BLOCK):
                row2.append(Bloc(8))
            if row[i].isinstance(D_BLOCK):
                row2.append(Bloc(9))
            blocklist2.append(row2)
    return blocklist2

def python_block_code(blocklist):
    return (code_utilisateur(graphic_to_model(blocklist)))
