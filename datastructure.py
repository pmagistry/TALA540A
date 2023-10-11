from dataclasses import dataclass

@dataclass
class Token:
    token_id: int
    text: str
    lemma: str
    pos: str
    dep: str
    head_id: int
    features: str

    def __str__(self):
        return f"{self.token_id}\t{self.text}\t{self.lemma}\t{self.pos}\t{self.features}\t_\t_\t{self.head_id}\t{self.dep}\t_"

    