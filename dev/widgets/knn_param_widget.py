from PySide6.QtCore import Qt
from PySide6.QtWidgets import  (QWidget, QGroupBox, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QScrollBar)
from __feature__ import snake_case, true_property
 
class KNNParamsWidget(QWidget):
    
    def __init__(self, fixed_width):
        super().__init__()
    
    # KNN Param -----------------------------------------------------------------------------------------
        self.knn_group = QGroupBox('Knn parameters')
        
        self.knn_group.set_fixed_width(fixed_width)
        self.knn_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        knn_group_layout = QVBoxLayout(self.knn_group)

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