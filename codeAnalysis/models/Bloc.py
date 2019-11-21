import codeAnalysis.models.config as cfg

class Bloc:
        
    def __init__(self,id,tab=None,prefix=None,suffix=None,condition=False,args=(None,None)):
        self.id=id
        self.tab=cfg.tab[min(id,5)]
        self.prefix=cfg.prefixes[id]
        self.suffix=cfg.suffixes[min(id,5)]
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
        global cfg.dico_calcul
        txt=self.text
        self.code = ''
        for i in range(len(txt)):
            if txt[i] in cfg.dico_calcul:
                self.code+=cfg.dico_calcul[txt[i]] 
            if 47<ord(txt[i])<58:
                self.code+=txt[i]
            if i>1 and 47<ord(txt[i-1])<58:
                self.code+='*'
            if i<len(txt)-1 and ord(txt[i])>64 and ord(txt[i+1])>64:
                self.code+=txt[i]+'*'
            elif ord(txt[i])>64 and txt[i] not in cfg.dico_calcul:
                self.code+=txt[i]
        return self.code
    def evaluate(self):
        exec("self.value="+self.python())
        return self.value


#argument est une liste qui contient les éventuels arguments du bloc: [nom_variable,valeur] ou [None,printable]
#tab est la tabulation relative après lecture de ce bloc


