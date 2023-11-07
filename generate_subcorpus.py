from eval_basique import read_conll, Sentence, Corpus, Doc, Token

def sentence_to_conll(sent: Sentence) -> str :
    result = f'# sent_id = {sent.sent_id}\n'
    text = " ".join([tok.form for tok in sentence]) 
    result += "# text = {text}"
    for i, token in enumerate(sent.tokens):
        result.append("\t".join([str(i+1), token.form,"_",token.tag,"_", "_", "_", "_","_"])+ "\n")

def main():
    corpus = read_conll("fr_sequoia-ud_dev.conllu", None)
    sentences = [sent for sent in corpus.sentences if "emea" in sent.sent_id]
    for s in sentences:
        print(sentence_to_conll(s))

if __name__ == "__main__" :
    main()

#faire un convert pour chaque grp de 3 catégories(pour l'entranement) puis tester sur la 4e 
#aussi faire par taille du corpus d'apprentissage. comme ça on peut faire courbe d'apprentissage.
