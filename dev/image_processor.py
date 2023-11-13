import numpy as np
from PySide6.QtGui import QImage
from klustr_utils import ndarray_from_qimage_argb32
import math


class ShapeCalculator:
    
    @staticmethod
    def perimeter(image):
        return np.sum(image[:, 1:] != image[:, :-1]) + \
            np.sum(image[1:, :] != image[:-1, :])

    @staticmethod
    def area(image):
        return np.sum(image)

    @staticmethod
    def centroid(image):
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        return (np.sum(r * image), np.sum(c * image)) / ShapeCalculator.area(image)

    @staticmethod
    def max_dist(image, coord):
        image = ShapeCalculator.__perimeter_array(image)
        c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        points = np.column_stack((c[image == 1], r[image == 1]))
        distances = np.linalg.norm(points - coord, axis=1)
        return np.amax(distances)

    @staticmethod
    def __perimeter_array(original_image):
        neighbors = np.array([(-1, 0), (0, -1), (1, 0), (0, 1)])
        
        shifted_images = [(np.roll(original_image, shift, axis=(0, 1)) == 0) 
                          for shift in neighbors]
        
        combined_shifted = np.logical_or.reduce(shifted_images)

        
        new_array = original_image & combined_shifted
        
        return new_array

class ImageProcessor:

    @staticmethod
    def get_shape(shape_name: str, shape_img: QImage):
        """Retourne le nom de la forme + les 3 determinants

        Args:
            shape_name (str): nom de la forme
            shape_img (QImage): image binaire

        Returns:
            list[str, np.ndarray, np.ndarray, np.ndarray]:
            liste contenant le nom de la forme et ses 3 determinants
        """
        img_array = ndarray_from_qimage_argb32(shape_img)

        # switch les 0 et les 1 pour que la forme soit remplie de 1
        img_array = 1 - img_array

        metric1 = ImageProcessor.__get_metric1(img_array)
        metric2 = ImageProcessor.__get_metric2(img_array)
        metric3 = ImageProcessor.__get_metric3(img_array)

        return [shape_name, metric1, metric2, metric3]

    @staticmethod
    def __get_metric1(img):
        area = area(img)
        perim = ShapeCalculator.perimeter(img)

        return (4 * math.pi * area) / (perim ** 2)

    @staticmethod
    def __get_metric2(img):
        center = ShapeCalculator.centroid(img)
        radius = ShapeCalculator.max_dist(img, center)
        circle_area = math.pi * radius ** 2

        metric2 = ShapeCalculator.area(img) / circle_area

        return metric2 if metric2 <= 1 else 1

    @staticmethod
    def __get_metric3(img):
        return ShapeCalculator.area(img) / (img.shape[0] * img.shape[1])
