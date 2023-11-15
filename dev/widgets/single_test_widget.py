from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import  (QWidget, QGroupBox, QLabel, QVBoxLayout, QSizePolicy, QPushButton, QComboBox)
from __feature__ import snake_case, true_property

class SingleTestWidget(QWidget):
    
    def __init__(self, fixed_width):
        super().__init__()
        
    #Single Text --------------------------------------------------------------------------------------
        self.test_group = QGroupBox('Single test')
        
        self.test_group.set_fixed_width(fixed_width)
        self.test_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        test_group_layout = QVBoxLayout(self.test_group)
        
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