import scatter_3d_viewer as q3

from klustr_dao import PostgreSQLKlustRDAO
from widgets.settings_widget import SettingsWidget

from scatter_3d_viewer import QColorSequence
from PySide6.QtCore import Slot
from PySide6.QtWidgets import  (QWidget, QHBoxLayout, QSizePolicy)
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
        
        self.settings_widget.dataset_widget.data_search_bar.currentIndexChanged.connect(self.__update_scatter)
    
    @Slot()
    def __update_scatter(self):
        self.__scatter.clear()
        knn = self.settings_widget.get_knn()
        knn_data = knn.data
        for i in range(0 , (knn_data[:,0].astype(int)).max()+1):
            data3d = knn_data[knn_data[:,0] == i]
            self.__scatter.add_serie(data3d[:,1:], QColorSequence.next(), knn.category[i]) #size_percent = 0.25
            
        #print(data3d)
