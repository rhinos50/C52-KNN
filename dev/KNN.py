import numpy as np

class KNN():
    def __init__(self, determinants, nb_data, k):
        self.__data = np.ndarray()
        self.__k = k
        self.__category = []

    """
    Méthode permettant d'ajouter des points aux données d'entrainement du KNN

    :parm list: Une liste python ou le premier argument est une string contenant la catégorie de la donné suivi de n déterminants
    """
    def add_point_(self, list):
        mat = self.__process_list(list)

    
    #
    def __process_list(self, list):

        if(list[0] not in self.__category):

        return np.ndarray(list)