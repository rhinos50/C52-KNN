import scatter_3d_viewer as q3
import image_processor as imp 
import KNN as knn
import numpy as np

from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding
from widgets.about_widget import AboutWindow

from scatter_3d_viewer import QColorSequence
from random import randint, choice
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Slot
from PySide6.QtWidgets import  (QWidget, QGroupBox, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton, QComboBox, QScrollBar)
from PySide6.QtGui import  (QImage, QPixmap)
from __feature__ import snake_case, true_property

class DatasetWidget(QWidget):
    
    def __init__(self, fixed_width, datasets):
        super().__init__()
        
        #DATASET -----------------------------------------------------------------------------------------
        self.dataset_group = QGroupBox('Dataset')
        
        self.dataset_group.set_fixed_width(fixed_width)
        self.dataset_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        dataset_group_layout = QVBoxLayout(self.dataset_group)
        
        #settings_layout.add_widget(dataset_group) #TODO

        self.data_search_bar = QComboBox()
        i = 0
        for row in datasets:
            i += 1
            item = row[1] + " [" + str(row[5]) +"][" + str(row[6] + row[7]) + "]"
            self.data_search_bar.insert_item(i, item, row)
        
        #included:
        info_group = QGroupBox('Included in dataset')
        test_group_layout = QVBoxLayout(info_group)
        
        category = QLabel("Category count:")
        training_img = QLabel("Training image count:")
        test_img = QLabel("Test image count:")
        total_img = QLabel("Total image count:")
        
        self.category_value = QLabel("0")
        self.training_img_value = QLabel("0")
        self.test_img_value = QLabel("0")
        self.total_img_value = QLabel("0")
        
        
        self.create_text_layout(category, self.category_value, test_group_layout)
        self.create_text_layout(training_img, self.training_img_value, test_group_layout)
        self.create_text_layout(test_img, self.test_img_value, test_group_layout)
        self.create_text_layout(total_img, self.total_img_value, test_group_layout)
        
        #transformation:
        transformation_group = QGroupBox('Transformation')
        transformation_layout = QVBoxLayout(transformation_group)
        
        translated = QLabel("Translated:")
        rotated = QLabel("Rotated:")
        scaled = QLabel("Scaled:")
        
        self.translated_value = QLabel("False")
        self.rotated_value = QLabel("False")
        self.scaled_value = QLabel("False")
        
        #compacted layouts
        self.create_text_layout(translated, self.translated_value, transformation_layout)
        self.create_text_layout(rotated, self.rotated_value, transformation_layout)
        self.create_text_layout(scaled, self.scaled_value, transformation_layout)
        
        #info_layout
        info_layout = QHBoxLayout()
        info_layout.add_widget(info_group)
        info_layout.add_widget(transformation_group)
        dataset_group_layout.add_widget(self.data_search_bar)
        dataset_group_layout.add_layout(info_layout)
        
    def create_text_layout(self, text, value, parent):
        layout = QHBoxLayout()
        layout.add_widget(text)
        layout.add_widget(value)
        parent.add_layout(layout)