# TALA540A

## 25 octobre 2023.

Comme j'ai la chance d'avoir un pc custom, j'ai reconfiguré un modèle pour qu'il utilise le gpu (les scripts et dossiers qui finissent par gpu du coup).
J'ai modifié le batch_size à 32, mis le max_epoch à 10 (je ne sais pas ce qui était le mieux) et le max_steps à 20500 (pareil que pour les epochs) = des LOSS TAGG énormes.
Donc j'ai recommencé en laissant le max_epoch à 0 et le max_steps à 20000 et en baissant la patience à 800 pour que ca s'arrête plus tot si le score ne s'améliore pas.

**Résultats** du train en classe au train avec gpu :
- TAGG_ACC : de 93.45 à 95.81
- Score : 0.93 à 0.96
- LOSS TAGG : 83.26 à 572.32
- LOSS TOK2VEC (cpu) : 4.07
- LOSS TRANS (gpu) : 266.30 

Il faudrait pouvoir réduire le loss.
+ pas pu push le modele car trop gros
