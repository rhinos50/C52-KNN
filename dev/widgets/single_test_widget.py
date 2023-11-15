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

class SingleTestWidget(QWidget):
    
    def __init__(self, fixed_width):
        super().__init__()
        
    #Single Text --------------------------------------------------------------------------------------
        self.test_group = QGroupBox('Single test')
        
        self.test_group.set_fixed_width(fixed_width)
        self.test_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        test_group_layout = QVBoxLayout(self.test_group)
        
        #settings_layout.add_widget(test_group)
        
        self.img_search_bar = QComboBox()
        
        self.img_search_bar.insert_item(0, "Select Dataset")
        test_group_layout.add_widget(self.img_search_bar)

        #Image
        self.view_label = QLabel()
        self.view_label.set_fixed_size(QSize(330, 180))
        self.view_label.style_sheet = 'QLabel { background-color : #313D4A; padding : 10px 10px 10px 10px; }' # 354A64
        self.view_label.alignment = Qt.AlignmentFlag.AlignCenter

        test_group_layout.add_widget(self.view_label)

        #button
        self.classify_button = QPushButton("Classify")
        test_group_layout.add_widget(self.classify_button)

        #text
        self.class_text = QLabel("Not Classified")
        self.class_text.alignment = Qt.AlignmentFlag.AlignCenter
        test_group_layout.add_widget(self.class_text)