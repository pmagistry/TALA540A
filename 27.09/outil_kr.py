from khaiii import KhaiiiApi 

# Création d'une instance de KhaiiiApi
api = KhaiiiApi()

# Identification des parties du discours
def pos(text):
    tokens = api.analyze(text)
    for word in tokens:
        print(word)

    api.close()

if __name__ == "__main__":
    text = "두 친구가 공원에서 산책하고 있었어요. 하늘은 맑고 파란색이었고, 바람이 부드럽게 불고 있었어요. 그들은 웃으면서 얘기를 나누었고, 즐거운 시간을 보냈어요."
    
    print("\nPartie du discours")
    pos(text)

