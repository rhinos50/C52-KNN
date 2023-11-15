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

class KNNParamsWidget(QWidget):
    
    def __init__(self, fixed_width):
        super().__init__()
    
    # KNN Param -----------------------------------------------------------------------------------------
        self.knn_group = QGroupBox('Knn parameters')
        
        self.knn_group.set_fixed_width(fixed_width)
        self.knn_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        knn_group_layout = QVBoxLayout(self.knn_group)
        
        #settings_layout.add_widget(knn_group)

        self.K_label = QLabel()
        self.K_scrollbar = QScrollBar()

        self.dist_label = QLabel()
        self.dist_scrollbar = QScrollBar()

        self.total_image_num = 50 

        K_layout = self.__create_scrollbar_layout('K =', self.K_scrollbar, self.K_label, self.total_image_num / 4)
        dist_layout = self.__create_scrollbar_layout('Max dist =', self.dist_scrollbar, self.dist_label, 20)

        knn_group_layout.add_layout(K_layout)
        knn_group_layout.add_layout(dist_layout)
        
    def __create_scrollbar_layout(self, title, scrollbar, value_label, sb_max_range):
        title_label = QLabel()

        title_label.text = title
        title_label.set_fixed_width(50)

        value_label.set_num(0)
        value_label.alignment = Qt.AlignmentFlag.AlignCenter
        value_label.set_fixed_width(30)

        scrollbar.set_range(0, sb_max_range) 
        scrollbar.value = 0
        scrollbar.orientation = Qt.Horizontal
        scrollbar.set_fixed_width(220)

        scrollbar.valueChanged.connect(value_label.set_num)
        
        layout = QHBoxLayout()
        layout.add_widget(title_label)
        layout.add_widget(value_label)
        layout.add_widget(scrollbar)

        return layout