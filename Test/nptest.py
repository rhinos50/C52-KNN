import numpy as np


def draw_rectangle(image, top_left, bottom_right):
    top_left = (max(0,top_left[0]), max(0,top_left[1]))
    bottom_right = (min(image.shape[1],bottom_right[0]), min(image.shape[0],bottom_right[1]))
    image[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]] = 1


def area(image):
  return np.sum(image)


def centroid(image):
  c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
  return (np.sum(r * image), np.sum(c * image)) / area(image)


def perimeter(image):
    return np.sum(image[:, 1:] != image[:, :-1]) + \
        np.sum(image[1:, :] != image[:-1, :])


def perimeter_array(image):
    img_per = np.logical_or(image[1:, 1:] != image[1:, :-1], image[1:, 1:] != image[:-1, 1:])
    img_per.dtype = image.dtype
    
    return np.sum(img_per), img_per


def draw_circle(image, center, radius):
  c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
  dist = np.sqrt((r-center[1])**2 + (c-center[0]) ** 2)
  circle = (dist <= radius).astype(np.uint8)
  image[:,:] = np.logical_or(image[:, :], circle)


if __name__ == '__main__':
    width = height = 30
    img = np.zeros((width, height), dtype=np.uint8)
    
    neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    n = np.array(neighbors)
    
    draw_rectangle(img, (5, 5), (15, 15))
    
    
    
    print(img[neighbors[0]])