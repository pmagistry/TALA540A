
import banglanltk
import csv
import banglanltk
from pprint import pprint
import regex
import bn_eval_basique
from bnlp import BengaliPOS
from sklearn.metrics import classification_report
import time



# extraction pos du corpus test conllu - avec banglanltk   
def format_banglanltk_pos(filepath):
    tokens = []
    sentences = []
    sid = ""
    spacy_bangla_dict = {}   
    with open('../pos/banglanltk_pos.txt', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            spacy_bangla_dict[row[0]]=row[-1] 
    with open(filepath, 'r') as f:
        bn_text = f.readlines()
        ids = bn_text[: : 3] # bn sentences 
        bn_lines = bn_text[1: : 3]    # roman translitertion
        translit_lines = bn_text[2: :3]
        
        for id, ben, translit in zip(ids, bn_lines, translit_lines ):
            ben= regex.sub('([.,!?])', r' \1 ', ben)
            translit= regex.sub('([.,!?])', r' \1 ', translit)
            for ben_word, translit_word in zip(ben.split(), translit.split()):
                pos = banglanltk.pos_tag(ben_word.strip())
                if pos in spacy_bangla_dict.keys():
                    posSpacy  = spacy_bangla_dict[pos]
                    # print(f'id = {id}   ben_word = {ben_word}   translit_word = {translit_word} pos = {posSpacy}')
                    tokens.append(bn_eval_basique.Token(translit_word, posSpacy, True))
            if len(tokens) != 0:
                sentences.append(bn_eval_basique.Sentence(sent_id=id.strip(), tokens=tokens))
                tokens=[]

    return bn_eval_basique.Corpus(sentences)


    
# extraction pos du corpus test conllu - avec bnlp     
def format_bnlp_pos(filePath):
    bn_pos = BengaliPOS()
    tokens = []
    sentences = []
    sid = ""
    bnlp_pos_dict = {}   
    # récupère équivalence de POS bnlp
    with open('../pos/bnlp_pos.txt', 'r', newline='', encoding='utf-8') as file:
        bnlp_pos = file.readlines()
        for row in bnlp_pos:
            row = row.split()
            bnlp_pos_dict[row[0]]=row[1] 
    with open(filePath, 'r') as f:
        bn_text = f.readlines()
        ids = bn_text[: : 3] # bn sentences 
        bn_lines = bn_text[1: : 3]    # roman translitertion
        translit_lines = bn_text[2: :3]
        
        for id, ben, translit in zip(ids, bn_lines, translit_lines ):
            ben = regex.sub('([.,!?])', r' \1 ', ben)
            translit= regex.sub('([.,!?])', r' \1 ', translit)
            pos_line = bn_pos.tag(ben)
            for word_pos_pair, translit_word in zip(pos_line, translit):
                if word_pos_pair[1]  in bnlp_pos_dict.keys():
                    pos = bnlp_pos_dict[word_pos_pair[1]]
                    tokens.append(bn_eval_basique.Token(translit_word, pos, True))
            if len(tokens) != 0:
                    sentences.append(bn_eval_basique.Sentence(sent_id=id.strip(), tokens=tokens))
                    tokens=[]
            # sentences.append(bn_eval_basique.Sentence(sent_id=id.strip(), tokens=tokens))
            
    return bn_eval_basique.Corpus(sentences)
 
 
            
# accuracy
def calculate_accuracy_and_report(gold_standard_corpus, predicted_corpus):
    y_true = []
    y_pred = []

    for gold_sentence, predicted_sentence in zip(gold_standard_corpus.sentences, predicted_corpus.sentences):
        for gold_token, predicted_token in zip(gold_sentence.tokens, predicted_sentence.tokens):
            y_true.append(gold_token.tag)
            y_pred.append(predicted_token.tag)

    accuracy = sum(1 for true, pred in zip(y_true, y_pred) if true == pred) / len(y_true) * 100
    classification_rep = classification_report(y_true, y_pred)
    return accuracy, classification_rep



# main # 
def main() :
    banglanltk_Corpus = format_banglanltk_pos('../corpus/bengali/bn_connll_txt.txt')
    bnlp_Corpus = format_bnlp_pos('../corpus/bengali/bn_connll_txt.txt')
    gold_corpus = bn_eval_basique.read_conll('../corpus/bengali/bn_bru-ud-test.conllu')
    
    accuracy, classification_report_str = calculate_accuracy_and_report(gold_corpus, banglanltk_Corpus)
    print("Annotation banglanltk vs. gold_corpus\nImpression de résultat : ")
    print(f"Accuracy: {accuracy:.2f}%")
    print("Classification Report:")
    print(classification_report_str)
            
    accuracy, classification_report_str = calculate_accuracy_and_report(gold_corpus, bnlp_Corpus)
    print("Annotation BNLP vs. gold_corpus\nImpression de résultat")
    print(f"Accuracy: {accuracy:.2f}%")
    print("Classification Report:")
    print(classification_report_str)
            
    

   
if __name__ == "__main__":
    main()
