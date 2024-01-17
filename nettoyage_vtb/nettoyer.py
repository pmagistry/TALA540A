import re

def nettoyer_phrase(phrase):
    # Supprimer les annotations entre parenthèses
    phrase = re.sub(r'\([^)]*\)', '', phrase)
    # Supprimer tous les "/" suivis de n'importe quel caractère
    phrase = re.sub(r'/\S', '', phrase)
    # Supprimer les underscores
    phrase = phrase.replace('_', ' ')
    return phrase

def traiter_fichier(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as fichier_entree:
        lignes = fichier_entree.readlines()

    phrases_nettoyees = [nettoyer_phrase(ligne) for ligne in lignes]

    with open(output_filename, 'w', encoding='utf-8') as fichier_sortie:
        fichier_sortie.write(' '.join(phrases_nettoyees))

# Exemple d'utilisation
input_file = 'vtb.txt'
output_file = 'vtb_nettoye.txt'

traiter_fichier(input_file, output_file)

