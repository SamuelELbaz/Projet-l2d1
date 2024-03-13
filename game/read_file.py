def read_file(file_path: str) -> list:
    """
    @param file_path: chemin d'un fichier
    @return: liste de str entre chaque "_" du nom de file_path (SEULEMENT LE NOM, NE PREND PAS EN COMPTE LE CHEMIN)
    """
    info = []
    ind = file_path.rindex("/")
    file_path = file_path[ind+1:]
    print(file_path)
    while file_path.count("_") > 0:
        i = file_path.index('_')
        info.append(file_path[:i])
        file_path = file_path[i+1:]
    ind = file_path.find('.')
    if not ind:
        info.append(file_path)
    else:
        info.append(file_path[:ind])
    return info


if __name__ == "__main__":
    info = read_file("C:/Users/Nuskise/Documents/Licence_2/projet_IA/TEST_2/game/neat-checkpoint/_1-2_speed_3.pkl")
    print(info)

