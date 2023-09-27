from underthesea import word_tokenize, pos_tag, chunk, dependency_parse, sentiment

text = "Nhà hàng Lan là nhà hàng nổi tiếng nhất trong khu phố"
translate = "Le restaurant de Lan est le restaurant le plus populaire/célèbre du quartier."
text_sent = "Đồ ăn nhà hàng thực sự không ngon."
trad_sent = "La nourriture du restaurant n'était vraiment pas bonne."
print(translate)
print(text)

token = word_tokenize(text)
print()
print(f'Tokenize : ', token)

word_token = word_tokenize(text, format="text")
print(word_token)
print()

# POS Tagging

pos = pos_tag(text)
print(f'POS Tagging : ', pos)
print()

# Chunking

chunk_t = chunk(text)
print(f'Chunking :', chunk_t)
print()

# Parsing

parsing = dependency_parse(text)
print(f'Parsing : ', parsing)
print()

# Sentiment ??

sentiment_t = sentiment(text_sent)
print(f'Phrase : ', text_sent)
print(f'Traduction : ', trad_sent)
print(f'Sentiment : ', sentiment_t)