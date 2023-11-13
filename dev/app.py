import sys


from db_credential import PostgreSQLCredential
from klustr_dao import PostgreSQLKlustRDAO
from classification_widget import ClassificationWidget
from klustr_widget import KlustRDataSourceViewWidget

from PySide6.QtWidgets import  (QApplication, QTabWidget)
from __feature__ import snake_case, true_property 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tabs = QTabWidget()
    credential = PostgreSQLCredential(
                      host='localhost', 
                      port=5432, 
                      database='postgres', 
                      user='postgres', 
                      password='AAAaaa123')
    klustr_dao = PostgreSQLKlustRDAO(credential)

    source_data_widget = KlustRDataSourceViewWidget(klustr_dao)

    tabs.add_tab(source_data_widget,"klustR Viewer")
    tabs.add_tab(ClassificationWidget(credential),"Classification")
    
    tabs.show()

    sys.exit(app.exec())    