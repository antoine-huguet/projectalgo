import config
class Bloc:
    def __init__(self,type,tab,prefix,suffix,condition=False,argument=[None,None]):
        self.type=type
        self.tab=tabs[i]
        self.prefix=prefixes[i]
        self.suffix=suffixes[i]
#argument est une liste qui contient les éventuels arguments du bloc: [nom,valeur] ou [None,printable]


def code_executable(block_list):
    code=[]
    t=0
    for bloc in blocklist:
        code.append(t*'\t')
        code.append(bloc.argument[0].name)
        code.append(bloc.prefix)
        code.append(str(bloc.argument[1]))
        code.append(txt.(bloc.condition()))
        code.append(bloc.suffixe)
        t=t+bloc.tab
    return(code.join())

def code_utilisateur(block_list):
    code=['from time import * \n']
    t=0
    for bloc in blocklist:
        code.append(t*'\t')
        code.append(bloc.argument[0].name)
        code.append(bloc.prefix)
        code.append(str(bloc.argument[1]))
        code.append(txt.(bloc.condition()))
        code.append(bloc.suffixe)
        t=t+bloc.tab
        if bloc.prefixe=='=':
            code.append(affiche(code.argument))
            code.append('\ntime.pause(.3)\n')
    return(code.join())
