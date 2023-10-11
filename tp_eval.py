import spacy
from spacy.tokens import Doc

class Word:
    def __init__(self,lst:list):
        self.id=lst[0]
        self.form=lst[1]
        self.lemma=lst[2]
        self.upos=lst[3]
        self.xpos=lst[4]
        self.feats=lst[5]
        self.head=lst[6]
        self.deprel=lst[7]
        self.deps=lst[8]
        self.misc=lst[9]

class confusionMatrix:
    def __init__(self,classes):
        self.matrix={predicted:{actual:0 for actual in classes}for predicted in classes}
        self.classes=classes
    def add(self,predicted,actual):self.matrix[predicted][actual]+=1
    def evaluate(self):
        allEvaluations={className:{"precision":[0,0],"recall":[0,0]}for className in self.classes}
        for predicted,actualValues in self.matrix.items():
            for actual,count in actualValues.items():
                if predicted==actual:
                    allEvaluations[predicted]["precision"][0]+=count
                    allEvaluations[predicted]["precision"][1]+=count
                    allEvaluations[predicted]["recall"][0]+=count
                    allEvaluations[predicted]["recall"][1]+=count
                else:
                    allEvaluations[predicted]["precision"][1]+=count
                    allEvaluations[actual]["recall"][1]+=count
        for className in allEvaluations.keys():
            allEvaluations[className]["precision"]=allEvaluations[className]["precision"][0]/allEvaluations[className]["precision"][1]if allEvaluations[className]["precision"][1]!=0 else -1
            allEvaluations[className]["recall"]=allEvaluations[className]["recall"][0]/allEvaluations[className]["recall"][1]if allEvaluations[className]["recall"][1]!=0 else -1
            P,R=allEvaluations[className]["precision"],allEvaluations[className]["recall"]
            allEvaluations[className]["f1-score"]=(2*P*R)/(P+R)if allEvaluations[className]["precision"]!=-1 and allEvaluations[className]["recall"]!=1 else -1
        return{"precision":avg([allEvaluations[className]["precision"]for className in allEvaluations.keys()]),
               "recall":avg([allEvaluations[className]["recall"]for className in allEvaluations.keys()]),
               "f1-score":avg([allEvaluations[className]["f1-score"]for className in allEvaluations.keys()])}

def avg(lst):return sum([ele for ele in lst if ele!=-1])/len([ele for ele in lst if ele!=-1])

#Reading file and Spacy annotation
nlp=spacy.load("fr_core_news_sm")
file=[Word(line.strip().split("\t"))for line in open("fr_sequoia-ud-test.conllu","r",encoding="utf-8").readlines()if line[0]!="#"and line.strip()!=""]
words=[word.form for word in file]
spaces=[False if word.misc=="SpaceAfter=No"else True for word in file]
doc=nlp(Doc(nlp.vocab,words,spaces))

#Evaluation
accuracy=[0,0]#nbr correct, total
for tokenSpacy,tokenFile in zip(doc,file):
    #if tokenSpacy.text!=tokenFile.form:input(f"Oulah, je crois qu'il y a un problème... Spacy:{tokenSpacy.text} et File:{tokenFile.form}")
    if tokenSpacy.pos_==tokenFile.upos:accuracy[0]+=1
    accuracy[1]+=1

matrix=confusionMatrix(set([token.pos_ for token in doc]+[token.upos for token in file]))
for tokenSpacy,tokenFile in zip(doc,file):
    matrix.add(tokenSpacy.pos_,tokenFile.upos)

matrix=matrix.evaluate()
print(f"""Accuracy = {round(accuracy[0]/accuracy[1]*100,2)}%
Precision = {round(matrix["precision"]*100,2)}%
Recall = {round(matrix["recall"]*100,2)}%
F1-score = {round(matrix["f1-score"]*100,2)}%""")