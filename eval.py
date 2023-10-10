

def load_conllu(file_path):
    """
    Charger les données conllu
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()

def compare_files(file_path1, file_path2):
    doc_ref = load_conllu(file_path1)
    doc_test = load_conllu(file_path2)
    
    total_tokens = len(doc_ref)
    
    correct_pos_tags = 0

    for line_ref, line_test in zip(doc_ref, doc_test):
        if line_ref.startswith("#") or line_test.startswith("#"):
            continue  # Ignore les lignes de commentaire

        parts_ref = line_ref.split('\t')
        parts_test = line_test.split('\t')

        if len(parts_ref) != len(parts_test):
            continue  # Ignore les lignes avec des colonnes de longueur différente

        # Comparaison de l'étiquette POS (colonne 3)
        pos_ref = parts_ref[3]
        pos_test = parts_test[3]

        if pos_ref == pos_test:
            correct_pos_tags += 1

    pos_accuracy = (correct_pos_tags / total_tokens) * 100

    return pos_accuracy


def main():
    file_path1 = "fr_sequoia-ud-test.conllu"
    file_path2 = "fr_sequoia-ud-test-tok.conllu"
    pos_accuracy = compare_files(file_path1, file_path2)
    
    print(f"Exactitude globale : {pos_accuracy:.2f}%")


if __name__ == "__main__":
    main()
