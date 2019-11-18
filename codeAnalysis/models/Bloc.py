
class Bloc:
    def __init__(self,id,tab=None,prefix=None,suffix=None,condition=False,args=(None,None)):
        self.id=id
        self.tab=tabs[id]
        self.prefix=prefixes[id]
        self.suffix=suffixes[id]
        if self.id==2:
            self.suffix=str(args[1])+')'
        self.condition=condition
        self.args=args
#argument est une liste qui contient les éventuels arguments du bloc: [nom_variable,valeur] ou [None,printable]
#tab est la tabulation relative après lecture de ce bloc


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

def code_utilisateur(block_list):
    code=[]
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
            #mise à jour de la liste des affectations et prints
        code.append('\n')
    return(''.join(code),L)

blocklist=[[Bloc(5),Bloc(3,args=('a',1))],[Bloc(6),Bloc(3,args=('b',2))],[Bloc(7),Bloc(3,args=('c',1))],[Bloc(8),Bloc(3,args=('d','b*b-4*a*c'))],[Bloc(2,args=(None,'d'))]]
#code qui print le discriminant de aX²+bX+c

file=open('code.py','w+')
file.write(code_utilisateur(blocklist)[0])
file.close()
#écriture du code associé à blocklist dans code.py