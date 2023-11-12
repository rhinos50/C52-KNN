import numpy as np

class KNN():
    def __init__(self, k, nb_determinant, dist_max):
        self.__nb_determinant = nb_determinant
        self._data = np.empty((0,nb_determinant+1), dtype=np.float16)
        self.__dist_max = dist_max
        self.__k = k
        self.__category = []

    """
    Méthode permettant d'ajouter des points aux données d'entrainement du KNN

    :parm new_point: Une liste python ou le premier argument est une string contenant la catégorie de la donné suivi de n déterminants
    """
    def add_point(self, new_point):
        mat = self.__process_list(new_point)
        self._data = np.vstack((self._data, mat))


    """
    Méthode permettant de classifier un point parmis les donnné d'entrainements

    :parm point: Une liste python ou le premier argument est une string contenant la catégorie de la donné suivi de n déterminants
    
    @return: Une String contenant la classification de la donné ou l'erreur survenue lors de la classifiaction
    """
    def classify(self, point):

        # trouver les distances
        self.__calculate_distances(point)

        # trouver les indices des k-nearest-neighbours
        distances = self._data[:, -1]
        nn_indices = np.argsort(distances)
        knn_indices = nn_indices[:self.__k-1] # -1 car les indices de colonnes commencent a 0

        # vérifier si les distances sont dans l'intervalle
        if (np.max(distances[knn_indices]) > self.__dist_max):
            return "Classification impossible car la aucune donné n'est comprise dans l'intervale de contrôle maximum"

        # Step 4: Get categories of k nearest neighbors
        nearest_neighbors_categories = self._data[knn_indices, 0]

        # Step 5: Find the most common category among k nearest neighbors
        predicted_category = np.bincount(nearest_neighbors_categories.astype(int)).argmax()

        return self.__category[predicted_category]

    def __process_list(self, list):
        if len(list) != self.__nb_determinant+1:
            raise ValueError("Le nombre de colonnes dans la nouvelle ligne ne correspond pas aux données contenu dans _data.")
        if(list[0] not in self.__category):
            self.__category.append(list[0])

        list[0] = self.__category.index(list[0]) 

        return np.array(list, dtype=np.float16).reshape(1, -1)
    
    def __calculate_distances(self, new_point):
        if len(new_point) != self.__nb_determinant:
            raise ValueError("Le nombres de déterminants du point a classifier ne correspond pas au nombre de déterminants des données d'entrainements")

        # Distances Euclidienne entre le point a classifier et toutes les autres points 
        distances = np.linalg.norm(self._data[:, 1:] - new_point, axis=1)
        distances = np.array(distances,dtype=np.float16).reshape(-1,1)
        self._data = np.hstack((self._data, distances))
    
#TODO: handle les cas limites
        
    
if __name__ == '__main__':
    knn = KNN(3, 3, 0.001)
    knn.add_point(['banana', 0.1, 0.2, 0.3])
    knn.add_point(['pudding', 0.4, 0.5, 0.6])
    knn.add_point(['pudding', 0.7, 0.8, 0.9])
    knn.add_point(['roche', 0.7, 0.8, 0.9])
    knn.add_point(['poil', 0.7, 0.8, 0.9])
    knn.add_point(['banana', 0.7, 0.8, 0.9])


    new_point = np.array([0.5, 0.6, 0.7], dtype=np.float16)
    print(knn.classify(new_point))

    

    print(knn._data)
