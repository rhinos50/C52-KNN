import scatter_3d_viewer as q3
import image_processor as imp
import KNN as knn
import numpy as np

from klustr_dao import PostgreSQLKlustRDAO
from klustr_utils import qimage_argb32_from_png_decoding

from scatter_3d_viewer import QColorSequence
from random import randint, choice
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import Slot
from PySide6.QtWidgets import  (QWidget, QGroupBox, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton, QComboBox, QScrollBar)
from PySide6.QtGui import  (QImage, QPixmap)
from __feature__ import snake_case, true_property

class ClassificationWidget(QWidget):
    
    def __init__(self, credential):
        super().__init__()
        
        self.sql_dao = PostgreSQLKlustRDAO(credential)
        
        self.__auto_title_count = 0
        self.__fixed_width = 350
        self.__scatter = q3.QScatter3dViewer()
        self.__scatter.title = 'Title'
        self.__scatter.axis_x.title = 'Roundness'
        self.__scatter.axis_y.title = 'Rapport de cercle'
        self.__scatter.axis_z.title = 'Densité'
        self.__scatter.shadow = q3.QScatter3dViewer.ShadowType.NoShadow
        
        self.__scatter.size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        #Settings Widget
        self.settings_widget = SettingsWidget(self.sql_dao)
        #layout: big layout
        layout = QHBoxLayout(self)
        layout.add_widget(self.settings_widget)
        layout.add_widget(self.__scatter)
        
        self.settings_widget.data_search_bar.currentIndexChanged.connect(self.__update_scatter)
              
              
    
    @Slot()
    def __test(self):
        self.__scatter.title = 'A test as title'
        self.__scatter.axis_x.title = 'Axis X'
        self.__scatter.axis_y.title = 'Axis Y'
        self.__scatter.axis_z.title = 'Axis Z'
        self.__scatter.axis_x.range = None
        self.__scatter.axis_y.range = (-1.0, 1.0)
        self.__scatter.axis_z.range = (0.0, 2.0)
        self.__scatter.shadow = q3.QScatter3dViewer.ShadowType.NoShadow
        self.__scatter.auto_rotate = True
        
        print(f'''
Title        : { self.__scatter.title }
Axis x       : { self.__scatter.axis_x.title } - range{ self.__scatter.axis_x.range }
Axis y       : { self.__scatter.axis_y.title } - range{ self.__scatter.axis_y.range }
Axis z       : { self.__scatter.axis_z.title } - range{ self.__scatter.axis_z.range }
Shadow       : { self.__scatter.shadow }
Auto-rotate  : { self.__scatter.auto_rotate }
Series count : { self.__scatter.series_count }
''')

    def __next_name(self):
                self.__auto_title_count += 1
                return f'Serie_{self.__auto_title_count:04}'
    
    @Slot()
    def __update_scatter(self):
        self.__scatter.clear()
        knn = self.settings_widget.get_knn()
        knn_data = knn.data
        for i in range(0 , (knn_data[:,0].astype(int)).max()+1):
            data3d = knn_data[knn_data[:,0] == i]
            self.__scatter.add_serie(data3d[:,1:], QColorSequence.next(), knn.category[i]) #size_percent = 0.25
            
        print(data3d)
       
        
        
            
class SettingsWidget(QWidget):
       
    def __init__(self, sql_dao):
        super().__init__()
        
        self.sql_dao = sql_dao
        self.datasets = self.sql_dao.available_datasets
        self.__fixed_width = 350
        self.knn = None
            
        #Setting: combine les 3 layouts ensemble
        settings_layout = QVBoxLayout(self)
        
#DATASET -----------------------------------------------------------------------------------------
        dataset_group = QGroupBox('Dataset')
        
        dataset_group.set_fixed_width(self.__fixed_width)
        dataset_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        dataset_group_layout = QVBoxLayout(dataset_group)
        
        settings_layout.add_widget(dataset_group)

        self.data_search_bar = QComboBox()
        i = 0
        for row in self.datasets:
            i += 1
            item = row[1] + " [" + str(row[5]) +"][" + str(row[6] + row[7]) + "]"
            self.data_search_bar.insert_item(i, item, row)
        
        self.data_search_bar.currentIndexChanged.connect(self.__update_data)
        
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
            
#Single Text --------------------------------------------------------------------------------------
        test_group = QGroupBox('Single test')
        
        test_group.set_fixed_width(self.__fixed_width)
        test_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        test_group_layout = QVBoxLayout(test_group)
        
        settings_layout.add_widget(test_group)
        
        self.img_search_bar = QComboBox()
        
        self.img_search_bar.insert_item(0, "Select Dataset")
        test_group_layout.add_widget(self.img_search_bar)

        #Image
        self.view_label = QLabel()
        self.view_label.set_fixed_size(QSize(330, 180))
        self.view_label.style_sheet = 'QLabel { background-color : #313D4A; padding : 10px 10px 10px 10px; }' # 354A64
        self.view_label.alignment = Qt.AlignmentFlag.AlignCenter

        test_group_layout.add_widget(self.view_label)
        self.img_search_bar.currentIndexChanged.connect(self.__update_image)

        #button
        self.classify_button = QPushButton("Classify")
        test_group_layout.add_widget(self.classify_button)

        #text
        self.class_text = QLabel("Not Classified")
        self.class_text.alignment = Qt.AlignmentFlag.AlignCenter
        test_group_layout.add_widget(self.class_text)
            
            
            
#KNN Param -----------------------------------------------------------------------------------------
        knn_group = QGroupBox('Knn parameters')
        
        knn_group.set_fixed_width(self.__fixed_width)
        knn_group.size_policy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        knn_group_layout = QVBoxLayout(knn_group)
        
        settings_layout.add_widget(knn_group)

        self.K_label = QLabel()
        self.K_scrollbar = QScrollBar()

        self.dist_label = QLabel()
        self.dist_scrollbar = QScrollBar()

        self.total_image_num = 50 

        K_layout = self.__create_scrollbar_layout('K =', self.K_scrollbar, self.K_label, self.total_image_num / 4)
        dist_layout = self.__create_scrollbar_layout('Max dist =', self.dist_scrollbar, self.dist_label, 20)

        knn_group_layout.add_layout(K_layout)
        knn_group_layout.add_layout(dist_layout)
        

# ABOUT -------------------------------------------------------------------------------------------

        self.about_button = QPushButton("About")
        settings_layout.add_widget(self.about_button)

# -------------------------------------------------------------------------------------------------

    def create_text_layout(self, text, value, parent):
        layout = QHBoxLayout()
        layout.add_widget(text)
        layout.add_widget(value)
        parent.add_layout(layout)

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
      
    @Slot()
    def __update_data(self):
        self.knn = knn.KNN(self.K_scrollbar.value, 3, 0.1)
        data = self.data_search_bar.current_data()
        
        self.total_image_num = data[6] + data[7]
        
        print(data)
        self.category_value.set_num(data[5])
        self.training_img_value.set_num(data[6])
        self.test_img_value.set_num(data[7])
        self.total_img_value.set_num(data[6] + data[7])
        
        self.translated_value.text = str(data[2])
        self.rotated_value.text = str(data[3])
        self.scaled_value.text = str(data[4])
        
        self.sql_dao.set_transformation_filters(False, True, False, False) #TODO SET TRANSFORMATION
        self.get_image_from_label(data[1])

        #update scrollbars
        self.K_scrollbar.set_range(0, (data[6] + data[7]) / 4)
        #self.dist_scrollbar.set_range(0, x)
        
    @Slot()
    def __update_image(self):
        img_data = self.img_search_bar.current_data() #image_list_info        
        image = qimage_argb32_from_png_decoding(img_data[6])
        self.view_label.pixmap = QPixmap.from_image(image)

    def get_image_from_label(self, dataset):

        labels = self.sql_dao.labels_from_dataset(dataset)
        #print(labels)
        i = 0
        self.img_search_bar.clear()
        for label in labels:
            images = self.sql_dao.image_from_label(label[0])
            for img in images:
                i += 1
                item = img[3] #img[3]: image_id
                self.img_search_bar.insert_item(i, item, img)
                self.knn.add_point(imp.ImageProcessor.get_shape(img[1], qimage_argb32_from_png_decoding(img[6])))
                # print(imp.ImageProcessor.get_shape(img[1], qimage_argb32_from_png_decoding(img[6])))
        print(self.knn.data)
        
    def get_knn(self):
        return self.knn
