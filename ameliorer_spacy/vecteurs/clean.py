# Ouvrir le fichier d'entrée en mode lecture
with open('vtb.txt', 'r', encoding='utf-8') as input_file:
    # Lire le contenu du fichier
    content = input_file.read()

# Diviser les paires mot/pos en utilisant l'espace comme séparateur
pairs = content.split()

# Nettoyer le contenu
cleaned_content = '\n'.join(s.split('/')[0] for s in pairs)
cleaned_content = cleaned_content.replace('/', ' ')

# Ouvrir le fichier de sortie en mode écriture
with open('vtb_cleaned.txt', 'w', encoding='utf-8') as output_file:
    # Écrire le contenu nettoyé dans le fichier de sortie
    output_file.write(cleaned_content)

print("Le nettoyage est terminé. Les résultats ont été enregistrés dans vtb_cleaned.txt.")
