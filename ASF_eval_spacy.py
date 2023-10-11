import spacy
import re

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("fr_core_news_sm")

def get_token(corpus, dico_gold):
    VP_lemme, VP_pos, FP_lemme, FP_pos = 0, 0, 0, 0
    cpt_total = 0
    #analyse morphology
    for phrase in corpus:
        doc = nlp(phrase)
        for token in doc:
                cpt_total +=1
                analyse = [token.text, token.lemma_, token.pos_]
                #print(analyse)
                new_VP_lemme, new_VP_pos, new_FP_lemme, new_FP_pos = compare_to_gold(dico_gold, analyse, phrase)
                VP_lemme += new_VP_lemme
                VP_pos += new_VP_pos
                FP_lemme += new_FP_lemme
                FP_pos += new_FP_pos
    return(VP_lemme, VP_pos, FP_lemme, FP_pos, cpt_total)

def compare_to_gold(dico_gold, analyse, phrase):
    #pour evaluer nous recuperons d'abord la phrase dans le dictionnaire puis nous chercons la forme afin de comparer lemme et pos
    token = analyse[0]
    VP_lemme, VP_pos, FP_lemme, FP_pos = 0, 0, 0, 0
    #lower gold_standard for more accurate results
    for key, value in dico_gold.items():
        if key == phrase:
            for forme, valeurs in value.items():
                if forme == token:
                    #evaluation par comparaison de tokens
                    if valeurs[0].lower() == analyse[1].lower():
                        #evaluation lemme
                        VP_lemme +=1
                    elif valeurs[0].lower() != analyse[1].lower():
                        #print(forme, "|", token, valeurs[0], valeurs[1], "| analyse :", analyse, " LEMME INCORRECT")
                        FP_lemme +=1
                    if valeurs[1].lower() == analyse[2].lower():
                        #evaluation_pos
                        print(valeurs[1], "POS detected")
                        VP_pos += 1
                    elif valeurs[1].lower() != analyse[2].lower():
                        FP_pos += 1
    #a relativiser : "au\t\t --> est ce ou non une erreur"
    return VP_lemme, VP_pos, FP_lemme, FP_pos

def get_sentences():
    # Process whole documents
    #plutot que de charger tout le document avec c.read() et c = open(doc, "r"), je fais un fichier contenant le texte à analyser
    liste_phrases = []
    with open("fr_sequoia-ud-test.conllu", "rt", encoding="utf-8") as c:
        text = c.read()
        pattern = r"# text = .*\.\n"
        match_string_text = re.findall(pattern, text)
        for e in match_string_text:
            e = e.replace("# text =", "")
            liste_phrases.append(e.strip())
    dico_gold = get_gold_standard(liste_phrases)
    return liste_phrases, dico_gold
		

def get_gold_standard(liste_phrases):
    dico_gold = {}
    f = open("fr_sequoia-ud-test.conllu", encoding="utf-8").readlines()
    for phrase in liste_phrases:
        for i in range(len(f)-1):
            if phrase in f[i]:
                #i est l'indice de la phrase en question dans le corpus
                annotation_in_sentence = []
                pattern_gold = r"^[0-9]+.*\n"
                i_prochain = i+1
                while True:
                    match = re.search(pattern_gold, f[i_prochain])
                    if i_prochain == len(f):
                        break
                    if match:
                        annotation_in_sentence.append(f[i_prochain])
                        #chaque ligne d'annotation après un texte
                        i_prochain +=1
                        continue
                    else:
                        break
                dico_gold = fill_dico(dico_gold, annotation_in_sentence, phrase)
    return dico_gold


def fill_dico(dico_gold, annotations, phrase):
    #dico_gold[phrase]={[forme]=[lemme, pos]}
    dico_gold[phrase]={}
    for e in annotations:
        e = e.split("\t")
        if len(e)>1:
            forme, lemme, pos = e[1], e[2], e[3]
            dico_gold[phrase][forme]=[lemme, pos]
    return dico_gold

    
            


if __name__ == "__main__":
    corpus, dico_gold = get_sentences()
    get_token(corpus, dico_gold)
    VP_lemme, VP_pos, FP_lemme, FP_pos, cpt_total = get_token(corpus, dico_gold)
    print("compte sans separation de classe", "\nVP_lemme = ", VP_lemme, "\n VP_pos = ", VP_pos, "FP_lemme = ", FP_lemme, "\n FP_pos = ", FP_pos, "\n cpt_total_tokens = ", cpt_total)
    pourcentage_lemmes_corrects = VP_lemme/cpt_total*100
    pourcentage_pos_corrects = VP_pos/cpt_total*100
    print("lemmes corrects :", pourcentage_lemmes_corrects)
    print("pos corrects : ", pourcentage_pos_corrects)