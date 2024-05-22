def check():
    import os
    # verifica se arq existe
    file = os.getcwd() + "/set_path_dir.txt"
    if os.path.isfile(file):
        infile = open(file, "r")
        path = infile.readline().strip() + "/"
        infile.close()
    else:
        print("set_path_dir.txt nao existe em ", file)
        exit()

    # verifica se diretorio existe
    if os.path.isdir(path) is False:
        print("nao encontrou diretorio em ", path)
        exit()

    return(path)


