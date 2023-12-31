import numpy as np

class ShapeCalculator:
    
    @staticmethod
    def perimeter(image: np.ndarray):
        """Retourne le perimetre de l'image"""
        return np.logical_or(
            (image[:, 1:] != image[:, :-1])[1:,:], 
            (image[1:, :] != image[:-1, :])[:,1:]).sum()


    @staticmethod
    def __centroid(image) -> tuple[float, float]:
        """Retourne le point centre de l'image"""
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        return (np.sum(r * image), np.sum(c * image)) / np.sum(image)

    @staticmethod
    def min_and_max(image: np.ndarray) -> tuple[float, float]:
        """Retourne une distance minimum et une distance maximum du centre
        de l'image et le point le plus proche et plus grand de cette dernière.

        Args:
            image (np.ndarray): matrice de l'image
    
        Returns:
            tuple(float, float): plus petite et plus grande distance
        """
       
        center = ShapeCalculator.__centroid(image)
        image = ShapeCalculator.__perimeter_array(image)
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        points = np.column_stack((r[image == 1], c[image == 1]))
        distances = np.linalg.norm(points - center, axis=1)
        return np.amin(distances), np.amax(distances)

    @staticmethod
    def __perimeter_array(image: np.ndarray) -> np.ndarray:
        """Retourne une matrice avec seulement les points du périmètre.
        
        
        IMPORTANT: ce n'est pas là même chose que la méthode perimeter, car 
        la somme des points du périmètre ne va pas donner la bonne valeur comparé
        à l'autre méthode
        """
        neighbors = np.array([(-1, 0), (0, -1), (1, 0), (0, 1)])
        
        shifted_images = [(np.roll(image, shift, axis=(0, 1)) == 0) 
                          for shift in neighbors]
        
        combined_shifted = np.logical_or.reduce(shifted_images)

        perim_array = image & combined_shifted
        
        return perim_array