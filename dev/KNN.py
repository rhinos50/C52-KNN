import numpy as np

class KNN():
    def __init__(self, k, nb_determinant, dist_max):
        self.__nb_determinant = nb_determinant
        self.data = np.empty((0,nb_determinant+1), dtype=np.float16)
        self.dist_max = dist_max
        self.k = k
        self.category = []
        
        self.first_time = True

    """
    Méthode permettant d'ajouter des points aux données d'entrainement du KNN

    :parm new_point: Une liste python ou le premier argument est une string contenant la catégorie de la donné suivi de n déterminants
    """
    def add_point(self, new_point):
        mat = self.__process_list(new_point)
        self.data = np.vstack((self.data, mat))

    def __process_list(self, list):
        if len(list) != self.__nb_determinant+1:
            raise ValueError("Le nombre de colonnes dans la nouvelle ligne ne correspond pas aux données contenu dans _data.")
        if(list[0] not in self.category):
            self.category.append(list[0])

        list[0] = self.category.index(list[0]) 

        return np.array(list, dtype=np.float16).reshape(1, -1)

    """
    Méthode permettant de classifier un point parmis les donnné d'entrainements

    :parm point: Une liste python de n déterminants
    
    @return: Une String contenant la classification de la donné ou l'erreur survenue lors de la classifiaction
    """
    def classify(self, point):
        # Souleve une exception si le nombre de déterminants ne corespond pas aux données d'entrainements
        if len(point) != self.__nb_determinant:
            raise ValueError("Le nombres de déterminants du point a classifier ne correspond pas au nombre de déterminants des données d'entrainements")
        
        # 1 - Trouver les distances
        self.__calculate_distances(point)

        # 2 - Trouver les indices des k-nearest-neighbours et leur distances
        distances = self.data[:, -1]
        nn_indices = np.argsort(distances)
        knn_indices = nn_indices[:self.k] # On peut utiliser self.__k car l'indice commence a 0 et le slicing exclue la borne externe
        knn_distances = distances[knn_indices]

        # 3 - CAS LIMITE: Vérifier et filtrer les distances pour sortir uniquement ceux dans l'intervalle de contrôle
        knn_indices = knn_indices[knn_distances <= self.dist_max]
        knn_distances = knn_distances[knn_distances <= self.dist_max]
        if (len(knn_distances)==0):
            return "Classification impossible car la aucune donné n'est comprise dans l'intervale de contrôle"

        # 4 - CAS LIMITE: vérifier si il y a des égalitées dans les résultats (retourne la categorie ayant la moyenne de distance la plus proche)
        knn_categories = self.data[knn_indices, 0] # Trouver les categories de k-nearest-neighbours
        category_counts = np.bincount(knn_categories.astype(dtype=np.int16))
        max_count = np.max(category_counts)
        tie_indexes = np.where(category_counts == max_count)[0] # On veut l'index 0 car category_counts est un 1d array donc retournera qu'un seul tuple contenant nos indices 

        if (len(tie_indexes) > 1):
            average_distances = []
            for index in tie_indexes:
                category_distances = knn_distances[knn_categories == index]
                avg_distance = np.mean(category_distances)
                average_distances.append(avg_distance)

            predicted_category = tie_indexes[np.argmin(average_distances)]
        else:
            predicted_category = tie_indexes[0]

        return self.category[predicted_category]
    
    def __calculate_distances(self, new_point):
        if(self.first_time):
            distances = np.linalg.norm(self.data[:, 1:] - new_point, axis=1) # Distances Euclidienne entre le point a classifier et toutes les autres points
            distances = np.array(distances,dtype=np.float16).reshape(-1,1) # reshape la matrice pour s'assurer qu'elle est de bonne taille pour le hStack 
            self.data = np.hstack((self.data, distances))
            self.first_time = False
        else:
            distances = np.linalg.norm(self.data[:, 1:-1] - new_point, axis=1) # Distances Euclidienne entre le point a classifier et toutes les autres points 
            distances = np.array(distances,dtype=np.float16).reshape(1,-1) # reshape la matrice pour s'assurer qu'elle est de bonne taille pour le hStack
            print(self.data[:,-1] )
            self.data[:,-1] = distances
        
        
           
if __name__ == '__main__':
    knn = KNN(7, 3, 0.001)
    knn.add_point(['banana', 0.11, 0.12, 0.13])
    knn.add_point(['banana', 0.13, 0.12, 0.11])
    knn.add_point(['banana', 0.12, 0.13, 0.11])
    knn.add_point(['pudding', 0.1, 0.12, 0.13])
    # knn.add_point(['pudding', 0.1, 0.12, 0.13])
    knn.add_point(['pudding', 0.24, 0.25, 0.26])
    knn.add_point(['pudding', 0.24, 0.25, 0.26])
    knn.add_point(['pudding', 0.24, 0.25, 0.26])
    knn.add_point(['roche', 0.11, 0.12, 0.13])
    knn.add_point(['roche', 0.41, 0.42, 0.43])
    knn.add_point(['poil', 0.51, 0.52, 0.53])
    
    new_point = np.array([0.5, 0.5, 0.5], dtype=np.float16)

    prediction = knn.classify(new_point)

    print(prediction)
    # print()
    # print(knn._data)
 

    