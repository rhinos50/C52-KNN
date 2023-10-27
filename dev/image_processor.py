import numpy as np
from PySide6.QtGui import QImage
from klustr_utils import ndarray_from_qimage_argb32
import math


def perimeter(image):
    return np.sum(image[:, 1:] != image[:, :-1]) + \
        np.sum(image[1:, :] != image[:-1, :])


def area(image):
    return np.sum(image)


def centroid(image):
    c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
    return (np.sum(r * image), np.sum(c * image)) / area(image)


def max_dist(image, coord):
    c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
    points = np.column_stack((c[image == 1], r[image == 1]))
    distances = np.linalg.norm(points - coord, axis=1)
    return np.amax(distances)


def draw_circle(image, center, radius):
    c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
    dist = np.sqrt((r-center[1])**2 + (c-center[0]) ** 2)
    circle = (dist <= radius).astype(np.uint8)
    image[:, :] = np.logical_or(image[:, :], circle)


def draw_rectangle(image, top_left, bottom_right):
    top_left = (max(0, top_left[0]), max(0, top_left[1]))
    bottom_right = (min(image.shape[1], bottom_right[0]), min(image.shape[0],
                                                              bottom_right[1]))
    image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = 1


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
        metric3 = None

        return [shape_name, metric1, metric2, metric3]

    @staticmethod
    def __get_metric1(img):
        area = np.sum(img)
        perim = perimeter(img)

        return 4 * math.pi * area / perim ** 2

    @staticmethod
    def __get_metric2(img):
        center = centroid(img)
        radius = max_dist(img, center)
        circle_area = math.pi * radius ** 2

        metric2 = np.sum(img) / circle_area

        return metric2 if metric2 <= 1 else 1


if __name__ == '__main__':
    # TEST
    original_array = np.zeros((20, 20), dtype=np.uint8)

    draw_rectangle(original_array, (10, 10), (15, 15))
    print(original_array)
    center = centroid(original_array)
    max = max_dist(original_array, center)

    circle_area = math.pi * max ** 2
    print(circle_area)
    print(np.sum(original_array))
    print(np.sum(original_array) / circle_area)
