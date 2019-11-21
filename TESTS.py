import codeAnalysis.models.Bloc as mbloc
import codeAnalysis.block_to_code as btc
import GUI.gui as gui
import GUI.models.Blocks as gbloc

gifblock=gbloc.IF_BLOCK(0,0)
calcul=gbloc.INPUT_BLOCK(0,0,"a=b")


b=mbloc.Bloc(0,condition=mbloc.Calcul_string(calcul.text))
ligne=[[gifblock,calcul],[gbloc.A_BLOCK(0,0),gbloc.AFFECTATION_BLOCK(0,0),gbloc.INPUT_BLOCK(0,0,"1")]]
#a=btc.graphic_to_model(ligne)
#print(a[0][0].condition)
#print (b)

ten=mbloc.Calcul_string("10")

print(mbloc.Bloc(2,args=(None,ten)).suffix)

#print(btc.code_utilisateur(a))