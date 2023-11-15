import sys 

from PySide6.QtWidgets import  (QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout)
from __feature__ import snake_case, true_property

class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_title = "About"
        self.about_widget = AboutWidget()
        
        self.set_central_widget(self.about_widget)

        
class AboutWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.about_layout = QVBoxLayout()
        
        self.title = QLabel()
        self.realised_by = QLabel()
        self.concepts = QLabel()
        self.descripteurs = QLabel()
        self.notions = QLabel()
        self.abstraction = QLabel()
        self.most_complex = QLabel()
        
        self.title.text = "Ce logiciel est le projet no 1 du cours C52 \n"
        
        self.realised_by.text = "Il a été réalisé par: \
                                \n- Noé Bousquet \
                                \n- Romain Fuoco-Binette \
                                \n- Maxime Desrochers \
                                \n- Emmanuel Senosier \n"
        
        self.concepts.text = "Il consiste à faire un algorithme de classification d'image binaire avec les concepts suivants: \
                                \n-Algorithme KNN \
                                \n-Vectorisation \
                                \n-Accès a une base de donnés \n"
        
        self.descripteurs.text = "Nos 3 descripteurs de forme sont: \
                                \n-Circularité \
                                    \n  -en ratio pour le domaine [0, 1] \
                                    \n  -correspondant à un ratio de l'aire de la forme par le périmètre au carré, plus la forme est ronde, plus la valeur tendera vers 1. \
                                \n-Ratio de cercle \
                                    \n  -en ratio pour le domaine [0, 1] \
                                    \n  -correspondant à un ratio d'un cercle englobant la forme par le cercle créé par la plus petite distance du centroide \
                                \n-Densité \
                                    \n  -en ratio pour le domaine [0, 1] \
                                    \n  -correspondant à un ratio de l'aire de la forme par l'aire du cercle qui l'englobe \n"
                                               
        self.notions.text = "Plus précisément, ce laboratoire permet de mettre en pratique les notions de: \
                            \n-Numpy \
                            \n-Pyside6 \
                            \n-SQL \
                            \n-Interface QT \n"
        
        self.abstraction.text = "Un effort d'abstraction a été fait pour ces points: \
                                \n-L'efficacité du KNN \
                                \n-La rapidité du programme \
                                \n-La précision des métriques \n"
        
        self.most_complex.text = "Finalement, l'ensemble de données le plus complexe que nous avons été capable de résoudre est: \
                                \n-Zoo-Large"
        
        
        self.about_layout.add_widget(self.title)
        self.about_layout.add_widget(self.realised_by)
        self.about_layout.add_widget(self.concepts)
        self.about_layout.add_widget(self.descripteurs)
        self.about_layout.add_widget(self.notions)
        self.about_layout.add_widget(self.abstraction)
        self.about_layout.add_widget(self.most_complex)        
        
        self.set_layout(self.about_layout)
        
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = AboutWindow()
    window.show()
    sys.exit(app.exec_())