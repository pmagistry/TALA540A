from pyvi import ViTokenizer, ViPosTagger
from pyvi import ViUtils

phrase = "Nhà hàng Lan là nhà hàng nổi tiếng nhất trong khu phố"

tok = ViTokenizer.tokenize(phrase)
print ("Voici la phrase tokénisée :", tok)

tag = ViPosTagger.postagging(ViTokenizer.tokenize(phrase))

#la ligne si on fait seulement un print : 
#print ("Voici les POS de chaque token :", tag)

# Affichez chaque token avec son POS (pour plus de lisibilité)
for token, tag in zip(tag[0], tag[1]):
    print(f" {{{token}, {tag} }}", end=';')
print ("\t")


sans_accents = ViUtils.remove_accents(phrase)
print("Voici la phrase sans accents :", sans_accents)

avec_accents = ViUtils.add_accents(u"Nha hang Lan la nha hang noi tieng nhat trong khu pho")
print("Voici la phrase avec des accents :", avec_accents)

