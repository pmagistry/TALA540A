from pprint import pprint
import random
import bn_eval_basique
from aksharamukha import transliterate


# transliteration 
def translit(word):
    translit = transliterate.process("Bengali", "IAST", word, nativize = True, pre_options = [], post_options = [])

    return translit


# export train et dev  en fichier conllu
def sentence_to_conll(sent, corpusType:str) -> str:
    result = f"# sent_id = {sent.sent_id}\n"
    text = " ".join([tok.form for tok in sent.tokens])
    result += f"# text = {text}\n"
    for i, token in enumerate(sent.tokens):
        result += "\t".join([str(i+1), token.form, "_", token.tag, "_", "_", "_", "_", "_", "_"]) + "\n"
        # result += "\t".join([str(i+1), token.form, "UNK", token.tag, "UNK", "UNK", "UNK", "UNK", "UNK", "UNK|UNK"]) + "\n"
        # append to file
    filepath = "../corpus/bengali/bn_" + corpusType + "_corpus.conllu" 
    with open(filepath, 'a') as fw:
        fw.write(result)
        
    return result


# lecture et construction de Corpus - corpus annoté (git) 
def read_nltr_corpus(textFile):
    pos_dict  = extract_pos_equivalence('../pos/bnlp_pos.txt')
    tokens = []
    sentences = []
    sid = 1
    with open(textFile, 'r') as f:
        file = f.readlines()
        
    for line in file:
        for word_pos in line.split():
            word_sep = str(word_pos).split('\\')
            if len(word_sep) > 1:
                word = word_sep[0]  
                word = translit(word)
                if type(word) is not str:
                    print(word)
                pos = word_sep[1].split('.')[0]
                if pos in pos_dict.keys():
                    pos_spacy = pos_dict[pos]
                    tokens.append(bn_eval_basique.Token(word, pos_spacy, True))
        if len(tokens) != 0:
            sentences.append(bn_eval_basique.Sentence(sent_id='sent_'+str(sid), tokens=tokens))
            tokens=[]
            sid +=1
            
    return bn_eval_basique.Corpus(sentences)
    
# dictionnaire  pos bnlp équivalence 
def extract_pos_equivalence(fileTxtPOS):
    bnlp_pos = {}
    with open (fileTxtPOS) as f:
        posline = f.readlines()
        for line in posline:
            line = line.split()
            pos_b, pos_spacy = line[0], line[1]
            bnlp_pos[pos_b] = pos_spacy
    return bnlp_pos


def main():
    whole_Corpus = read_nltr_corpus('../corpus/bengali/bn_nltr_pos_corpus.txt')
    whole_corpus = whole_Corpus.sentences  
    random.seed(42)
    random.shuffle(whole_corpus)
    split_index = int(0.8 * len(whole_corpus))
    # création train et dev .conllu à partir du corpus annoté 
    train_set = whole_corpus[:split_index]
    for sent in train_set:
        sentence_to_conll(sent, "train")
    dev_set = whole_corpus[split_index:]
    for sent in dev_set:
        sentence_to_conll(sent, "dev")

        
        


if __name__ == "__main__":
    main()
    
    
    
    
