

class Bloc:
    prefixes=['if','while','print(','=','','','A','B','C','D']
    suffixes=[':',':',')','','','','','','','']
    tabs=[1,1,0,0,-1,0,0,0,0,0]
    dico_calcul={'.':'*','*':'*','/':'/', '%':'%','^':'**', '²':'*2','+':'+','-':'-'}
    
    def __init__(self,id,tab=None,prefix=None,suffix=None,condition=False,args=(None,None)):
        self.id=id
        self.tab=tabs[id]
        self.prefix=prefixes[id]
        self.suffix=suffixes[id]
        if self.id==2:
            self.suffix=str(args[1])+')'
        self.condition=condition
        self.args=args



class Calcul_string(Bloc):
    def __init__(self,text):
        super().__init__(6)
        self.text=text
        self.code=''
        self.value = None
    def python(self):
        txt=self.text
        self.code = ''
        for i in range(len(txt)):
            if txt[i] in Bloc.dico_calcul:
                self.code+=dico_calcul[txt[i]] 
            if 47<ord(txt[i])<58:
                self.code+=txt[i]
            if i>1 and 47<ord(txt[i-1])<58:
                self.code+='*'
            if i<len(txt)-1 and ord(txt[i])>64 and ord(txt[i+1])>64:
                self.code+=txt[i]+'*'
            elif ord(txt[i])>64 and txt[i] not in dico_calcul:
                self.code+=txt[i]
        return self.code
    def evaluate(self):
        exec("self.value="+self.python())
        return self.value
            


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
        display_print(args[1])
    else:
        if args[1].uses_variables:
            string= str(args[0])+'='+args[1].text +'=' +str(evaluate.args[1])
        else:
            string= str(args[0])+'='+args[1].text
        display_affectation(string)


blocklist=[[Bloc(5),Bloc(3,args=('a',1))],[Bloc(6),Bloc(3,args=('b',2))],[Bloc(7),Bloc(3,args=('c',1))],[Bloc(8),Bloc(3,args=('d','b*b-4*a*c'))],[Bloc(2,args=(None,'d'))]]
#code qui print le discriminant de aX²+bX+c