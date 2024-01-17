from bn_eval_basique import read_conll, Sentence, Corpus, Token


def sentence_to_conll(sent: Sentence) -> str:
    result = f"# sent_id = {sent.sent_id}\n"
    text = " ".join([tok.form for tok in sent.tokens])
    result += f"# text = {text}\n"
    for i, token in enumerate(sent.tokens):
        result += "\t".join([str(i+1), token.form, "_", token.tag, "_", "_", "_", "_", "_", "_"]) + "\n"
    with open('corpus/bengali/bn_train_corpus.conllu', 'a') as fw:
            fw.write(result)
            
    return result



def main():
    corpus = read_conll("corpus/french/fr_sequoia-ud-dev.conllu", None)
    sentences = [ sent for sent in corpus.sentences if "emea" in sent.sent_id ]
    for s in sentences:
        print(sentence_to_conll(s))


if __name__ == "__main__":
    main()
