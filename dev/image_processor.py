import numpy as np
from PySide6.QtGui import QImage
from klustr_utils import ndarray_from_qimage_argb32

from utils.shapecalculator import ShapeCalculator


class ImageProcessor:

    @staticmethod
    def get_shape(shape_name: str, shape_img: QImage) -> tuple(str, float, float, float):
        """Retourne le nom de la forme + les 3 determinants

        Args:
            shape_name (str): nom de la forme
            shape_img (QImage): image binaire

        Returns:
            tuple[str, np.ndarray, np.ndarray, np.ndarray]:
            tuple contenant le nom de la forme et ses 3 determinants
        """
        img_array = ndarray_from_qimage_argb32(shape_img)

        # switch les 0 et les 1 pour que la forme soit remplie de 1
        img_array = 1 - img_array

        metric1 = ImageProcessor.__roundness(img_array)
        metric2 = ImageProcessor.__circle_rapport(img_array)
        metric3 = ImageProcessor.__get_metric3(img_array)

        return (shape_name, metric1, metric2, metric3)

    @staticmethod
    def __roundness(img: np.ndarray) -> float:
        """Retourne la circularité de l'aire et circonférence du cercle

        Args:
            img (np.ndarray): matrice de l'image

        Returns:
            float: ratio de la circularité
        """
        area = np.sum(img)
        perim = ShapeCalculator.perimeter(img)

        return (4 * np.pi * area) / (perim ** 2)

    @staticmethod
    def __circle_rapport(img: np.ndarray) -> float:
        """Retourne un rapport de l'air de du petit cercle sur l'aire du grand cercle
        créés avec le centre de l'image et la plus petite et grande distance de cette dernière.

        Args:
            img (np.ndarray): matrice de l'image

        Returns:
            float: ratio du rapport
        """
        
        min_radius, max_radius = ShapeCalculator.min_and_max(img)
        small_circle_area = np.pi * min_radius ** 2
        big_circle_area = np.pi * max_radius ** 2

        metric2 = small_circle_area / big_circle_area

        return metric2 

    @staticmethod
    def __get_metric3(img: np.ndarray) -> float:
        return np.sum(img) / (img.shape[0] * img.shape[1])

