import codeAnalysis.models.Bloc
import GUI.models.Blocks
import GUI.gui as gui

def code_executable(blocklist):
    code=[]
    t=0
    for row in blocklist:
        for bloc in row:
            code.append(t*'\t')
            code.append(bloc.prefix)
            code.append(str(bloc.args[1]))
            #code.append((bloc.condition.python()))
            code.append(bloc.suffix)
            t=t+bloc.tab
            code.append('\n')
    return(''.join(code))

def code_utilisateur(blocklist):
    code=['from time import sleep\n']
    L=[]
    t=0
    for row in blocklist:
        for bloc in row:
            code.append(t*'\t')
            code.append(bloc.prefix)
            if bloc.args[0]!=None:
                code.append(bloc.args[1].python())
            if bloc.condition !=None:    
                code.append(bloc.condition.text)
            code.append(bloc.suffix)
            #transcription d'une ligne dans l'ordre préfixe::condition::argument::suffixe
            t=t+bloc.tab
            if bloc.id==3 or bloc.id==4:
                L.append(bloc.args)
                code.append('\n sleep(.2) \n display(bloc.args)')
            #mise à jour de la liste des affectations et prints, pause et affichage
        code.append('\n')
    return(''.join(code))

def display(args):
    if args[0]==None:
        gui.writePrint(args[1])
    else:
        if args[1].uses_variables:
            string= str(args[0])+'='+args[1].text +'=' +str(args[1].evaluate())
        else:
            string= str(args[0])+'='+args[1].text
        gui.writeAffection(string)

def graphic_to_model(blocklist):
    blocklist2=[]
    for row in blocklist:
        row2=[]
        for i in range(len(row)):
            if i<len(row)-1 and isinstance(row[i],GUI.models.Blocks.IF_BLOCK):
                if isinstance(row[i+1],GUI.models.Blocks.INPUT_BLOCK):
                    a=codeAnalysis.models.Bloc.Bloc(0,condition=codeAnalysis.models.Bloc.Calcul_string(row[i+1].text))
                    print(a)
                    row2.append(a)
                else:
                    pass
                    #row2.append(codeAnalysis.models.Bloc.Bloc(0,condition=''.join([a.prefix for a in row[i+1:]])))
            if i<len(row)-1 and isinstance(row[i],GUI.models.Blocks.WHILE_BLOCK):
                if isinstance(row[i+1],GUI.models.Blocks.INPUT_BLOCK):
                    row2.append(codeAnalysis.models.Bloc.Bloc(1,condition=codeAnalysis.models.Bloc.Calcul_string(row[i+1].text)))
                else:
                    pass
                    #row2.append(codeAnalysis.models.Bloc.Bloc(1,condition=''.join([a.prefix for a in row[i+1:]])))
            if 0<i<len(row)-1 and isinstance(row[i],GUI.models.Blocks.AFFECTATION_BLOCK):
                if isinstance(row[i+1],GUI.models.Blocks.INPUT_BLOCK):
                    row2.append(codeAnalysis.models.Bloc.Bloc(3,args=[row2[i-1].prefix,codeAnalysis.models.Bloc.Calcul_string(row[i+1].text)]))
                else:
                    pass
                    #row2.append(codeAnalysis.models.Bloc.Bloc(3,args=[row2[i-1].prefix,''.join([a.prefix for a in row[i+1:]])]))
            if isinstance(row[i],GUI.models.Blocks.PRINT_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(2,args=[None,codeAnalysis.models.Bloc.Calcul_string(row[i+1].text)]))
            if isinstance(row[i],GUI.models.Blocks.INPUT_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Calcul_string(row[i].text))
            if isinstance(row[i],GUI.models.Blocks.ELSE_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(4))
            if isinstance(row[i],GUI.models.Blocks.END_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(5))
            if isinstance(row[i],GUI.models.Blocks.A_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(6))
            if isinstance(row[i],GUI.models.Blocks.B_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(7))
            if isinstance(row[i],GUI.models.Blocks.C_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(8))
            if isinstance(row[i],GUI.models.Blocks.D_BLOCK):
                row2.append(codeAnalysis.models.Bloc.Bloc(9))
        blocklist2.append(row2)
    return blocklist2

def python_block_code(blocklist):
    return (code_utilisateur(graphic_to_model(blocklist)))
