with open('train1.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

new_lines = []

for line in lines:
    parts = line.strip().split('\t')
    
    # Si la ligne a deux mots dans la première colonne
    if len(parts[0].split()) == 2:
        word1, word2 = parts[0].split()
        tag = parts[2]

        if tag == 'O':
            # Remplacer les tags "O" par "B-E" pour le premier mot et "I-E" pour le deuxième mot
            new_lines.append(f'{word1}\t{parts[1]}\tB-E')
            new_lines.append(f'{word2}\t{parts[1]}\tI-E')
        else:
            # Ajouter la première ligne sans modification
            new_lines.append(f'{word1}\t{parts[1]}\t{tag}')
            
            # Ajouter la deuxième ligne avec le tag "I-"
            new_lines.append(f'{word2}\t{parts[1]}\tI-{tag[2:]}')
    elif len(parts[0].split()) == 3:
        word1, word2, word3 = parts[0].split()
        tag = parts[2]
        
        if tag == 'O':
            new_lines.append(f'{word1}\t{parts[1]}\tB-E')
            new_lines.append(f'{word2}\t{parts[1]}\tI-E')
            new_lines.append(f'{word3}\t{parts[1]}\tI-E')
        else:
            # Ajouter la première ligne sans modification
            new_lines.append(f'{word1}\t{parts[1]}\t{tag}')
            
            # Ajouter la deuxième ligne avec le tag "I-"
            new_lines.append(f'{word2}\t{parts[1]}\tI-{tag[2:]}')
            new_lines.append(f'{word3}\t{parts[1]}\tI-{tag[2:]}')
    elif len(parts[0].split()) == 4:
        word1, word2, word3, word4 = parts[0].split()
        tag = parts[2]
        
        if tag == 'O':
            new_lines.append(f'{word1}\t{parts[1]}\tB-E')
            new_lines.append(f'{word2}\t{parts[1]}\tI-E')
            new_lines.append(f'{word3}\t{parts[1]}\tI-E')
            new_lines.append(f'{word4}\t{parts[1]}\tI-E')
        else:
            # Ajouter la première ligne sans modification
            new_lines.append(f'{word1}\t{parts[1]}\t{tag}')
            
            # Ajouter la deuxième ligne avec le tag "I-"
            new_lines.append(f'{word2}\t{parts[1]}\tI-{tag[2:]}')
            new_lines.append(f'{word3}\t{parts[1]}\tI-{tag[2:]}')
            new_lines.append(f'{word4}\t{parts[1]}\tI-{tag[2:]}')
    elif len(parts[0].split()) == 5:
        word1, word2, word3, word4, word5 = parts[0].split()
        tag = parts[2]
        
        if tag == 'O':
            new_lines.append(f'{word1}\t{parts[1]}\tB-E')
            new_lines.append(f'{word2}\t{parts[1]}\tI-E')
            new_lines.append(f'{word3}\t{parts[1]}\tI-E')
            new_lines.append(f'{word4}\t{parts[1]}\tI-E')
            new_lines.append(f'{word5}\t{parts[1]}\tI-E')
        else:
            # Ajouter la première ligne sans modification
            new_lines.append(f'{word1}\t{parts[1]}\t{tag}')
            
            # Ajouter la deuxième ligne avec le tag "I-"
            new_lines.append(f'{word2}\t{parts[1]}\tI-{tag[2:]}')
            new_lines.append(f'{word3}\t{parts[1]}\tI-{tag[2:]}')
            new_lines.append(f'{word4}\t{parts[1]}\tI-{tag[2:]}')
            new_lines.append(f'{word5}\t{parts[1]}\tI-{tag[2:]}')
    else:
        new_lines.append(line.strip())

# Écrire les résultats dans un nouveau fichier
with open('train_clean.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(new_lines))
