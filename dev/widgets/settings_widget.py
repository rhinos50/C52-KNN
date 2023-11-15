import image_processor as imp 
import KNN as knn

from klustr_utils import qimage_argb32_from_png_decoding

from widgets.dataset_widget import DatasetWidget
from widgets.single_test_widget import SingleTestWidget
from widgets.knn_param_widget import KNNParamsWidget
from widgets.about_widget import AboutWindow

from PySide6.QtCore import Slot
from PySide6.QtWidgets import  (QWidget, QVBoxLayout, QPushButton)
from PySide6.QtGui import  QPixmap
from __feature__ import snake_case, true_property

class SettingsWidget(QWidget):
       
    def __init__(self, sql_dao):
        super().__init__()
        
        self.sql_dao = sql_dao
        self.datasets = self.sql_dao.available_datasets
        self.__fixed_width = 350
        self.knn = None
        self.current_image = None
            
        #Setting: combine les 3 layouts ensemble
        settings_layout = QVBoxLayout(self)

# DATASET -----------------------------------------------------------------------------------------

        self.dataset_widget = DatasetWidget(self.__fixed_width, self.datasets)
        settings_layout.add_widget(self.dataset_widget.dataset_group)
        
        self.dataset_widget.data_search_bar.currentIndexChanged.connect(self.__update_data)
        
# Single Text --------------------------------------------------------------------------------------

        self.single_test_widget = SingleTestWidget(self.__fixed_width)
        settings_layout.add_widget(self.single_test_widget.test_group)
        
        self.single_test_widget.img_search_bar.currentIndexChanged.connect(self.__update_image)
        self.single_test_widget.classify_button.clicked.connect(self.__classify)

# KNN Param -----------------------------------------------------------------------------------------

        self.knn_params_widget = KNNParamsWidget(self.__fixed_width)
        settings_layout.add_widget(self.knn_params_widget.knn_group)

# ABOUT -------------------------------------------------------------------------------------------

        self.about_button = QPushButton("About")
        settings_layout.add_widget(self.about_button)
        self.about_button.clicked.connect(self.__show_about_window)

# -------------------------------------------------------------------------------------------------

    @Slot()
    def __show_about_window(self):
        self.window = AboutWindow()
        self.window.show()
      
    @Slot()
    def __update_data(self):
        self.knn = knn.KNN(self.knn_params_widget.K_scrollbar.value, 3, 0.8)
        data = self.dataset_widget.data_search_bar.current_data()
        
        self.total_image_num = data[6] + data[7]
        
        #print(data)
        self.dataset_widget.category_value.set_num(data[5])
        self.dataset_widget.training_img_value.set_num(data[6])
        self.dataset_widget.test_img_value.set_num(data[7])
        self.dataset_widget.total_img_value.set_num(data[6] + data[7])
        
        self.dataset_widget.translated_value.text = str(data[2])
        self.dataset_widget.rotated_value.text = str(data[3])
        self.dataset_widget.scaled_value.text = str(data[4])
        
        self.sql_dao.set_transformation_filters(False, True, False, False) #TODO SET TRANSFORMATION
        self.get_image_from_label(data[1])

        #update scrollbars
        self.knn_params_widget.K_scrollbar.set_range(0, (data[6] + data[7]) / 4)
        self.knn_params_widget.K_scrollbar.value = ((data[6] + data[7]) / 4) / 3
        self.knn.k = self.knn_params_widget.K_scrollbar.value
        
        self.knn_params_widget.dist_scrollbar.set_range(0.0, 1.0)
        
    @Slot()
    def __update_image(self):
        img_data = self.single_test_widget.img_search_bar.current_data() #image_list_info        
        image = qimage_argb32_from_png_decoding(img_data[6])
        self.single_test_widget.view_label.pixmap = QPixmap.from_image(image)
    
    @Slot()
    def __classify(self):
        img_data = self.single_test_widget.img_search_bar.current_data()
        processed_image = imp.ImageProcessor.get_shape(img_data[1], qimage_argb32_from_png_decoding(img_data[6]))
        
        self.single_test_widget.class_text.text = self.knn.classify(processed_image[1::]) 
        
        #update KNN parameters:
        self.knn.k = self.knn_params_widget.K_scrollbar.value


    def get_image_from_label(self, dataset):

        training_images = self.sql_dao.image_from_dataset(dataset, True)
        test_images = self.sql_dao.image_from_dataset(dataset, False)
        #print(labels)
        i = 0
        self.single_test_widget.img_search_bar.clear()
        for img in test_images:
            i += 1
            item = img[3] #img[3]: image_id
            self.single_test_widget.img_search_bar.insert_item(i, item, img)
        
       
        [self.knn.add_point(imp.ImageProcessor.get_shape(img[1], qimage_argb32_from_png_decoding(img[6]))) for img in training_images]  
       

    def get_knn(self):
        return self.knn