def remove_last_columns(input_file, output_file, delimiter='\t', num_columns_to_remove=2):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Supprimer les deux dernières colonnes
            columns = line.strip().split(delimiter)
            new_line = delimiter.join(columns[:-1]) + '\n'
            outfile.write(new_line)

# Spécifiez le nom de votre fichier d'entrée et de sortie
input_file_name = 'dev1.txt'
output_file_name = 'dev2.txt'

# Appel de la fonction pour supprimer les deux dernières colonnes
remove_last_columns(input_file_name, output_file_name)

