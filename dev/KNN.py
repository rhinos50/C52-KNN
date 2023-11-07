import numpy as np

class KNN():
    def __init__(self, k, nb_determinant):
        self.nb_determinant = nb_determinant
        self.__data = np.empty((0,nb_determinant+1), dtype=np.float16)
        self.__k = k
        self.__category = []

    """
    Méthode permettant d'ajouter des points aux données d'entrainement du KNN

    :parm list: Une liste python ou le premier argument est une string contenant la catégorie de la donné suivi de n déterminants
    """
    def add_point(self, list):
        mat = self.__process_list(list)
        self.__data = np.vstack((self.__data, mat))

    
    #
    def __process_list(self, list):
        if len(list) != self.nb_determinant+1:
            raise ValueError("Number of columns in the new row does not match the existing data.")
        if(list[0] not in self.__category):
            self.__category.append(list[0])

        list[0] = self.__category.index(list[0]) 

        return np.array(list, dtype=np.float16).reshape(1, -1)
    

#TODO: calculer distance d'une row avec tout les row de self.__data qui est nos training 
#      data et les stocker en tuple avec leur indice de row et leur distance (incice,dist)
#TODO: trouver les k plus proches voisins 
#TODO: trouver sa calssification a partir des indice 0 des k plus proche voisins et de self.__category
#TODO: handle les cas limites
#TODO: 
        
    
if __name__ == '__main__':
    knn = KNN(3, 3)
    knn.add_point(['banana', 0.1, 0.2, 0.3])
    knn.add_point(['pudding', 0.4, 0.5, 0.6])
    knn.add_point(['pudding', 0.7, 0.8, 0.9])
    knn.add_point(['roche', 0.7, 0.8, 0.9])
    knn.add_point(['poil', 0.7, 0.8, 0.9])
    knn.add_point(['banana', 0.7, 0.8, 0.9])


    # knn.add_point(['banana', 0.7, 0.8])

    print(knn.__data)