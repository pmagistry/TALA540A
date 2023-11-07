from eval_basique import read_conll, Sentence, Corpus, Token
import re

def sentence_to_conll(sent: Sentence) -> str:
    result = f"# sent_id = {sent.sent_id}\n"
    text = " ".join([tok.form for tok in sent.tokens])
    result += f"# text = {text}\n"
    for i, token in enumerate(sent.tokens):
        result += "\t".join([str(i+1), token.form, "_", token.tag, "_", "_", "_", "_", "_"]) + "\n"
    return result



def main():
    ids = ["emea", "Europar","frwiki", "annodis"]
    corpus = read_conll("train_spacy/fr_sequoia-ud-dev.conllu", None)
    for i in range(len(ids)) :
        excluded_index = i
        three_cat = ids[:excluded_index] + ids[excluded_index+1:]
        cat_1 = three_cat[0]
        cat_2 = three_cat[1]
        cat_3 = three_cat[2]
        with open(f"train_spacy/3_cat_corpus/3_cat_corpus_{cat_1}_{cat_2}_{cat_3}-dev.conllu", "w") as file:
            sentences = [ sent for sent in corpus.sentences if  re.split(r"\.|_|-",sent.sent_id)[0] in three_cat ]
            for s in sentences:
                file.write(sentence_to_conll(s))
                
                print(sentence_to_conll(s))


if __name__ == "__main__":
    main()
