prefixes=['if','while','print(','=','']
suffixes=[':\n',':\n',')\n',]
class bloc:
    def __init__(self,type,tab,prefix,suffix='\n',condition=False,argument=[None,None]):
        self.type=type
        self.tab=tab
        self.prefix=prefix

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

def code_utilisateur(block_list):
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
        if bloc.prefixe=='=':
            code.append(affiche(code.argument))
            code.append('\npause(.3)\n')

