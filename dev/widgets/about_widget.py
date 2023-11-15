import sys 

from random import randint, choice
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
        
        self.concepts.text = "Il consiste à faire __quelque_chose__ avec les concepts suivants: \
                                \n-__concept_1__ \
                                \n-__concept_n__ \n"
        
        self.descripteurs.text = "Nos 3 descripteurs de forme sont: \
                                \n-Roundness \
                                    \n  -en __unité__ pour le domaine __domaine__ \
                                    \n  -correspondant à __courte_description__ \
                                \n-Circle Ratio \
                                    \n  -en __unité__ pour le domaine __domaine__ \
                                    \n  -correspondant à __courte_description__ \
                                \n-Densité \
                                    \n  -en __unité__ pour le domaine __domaine__ \
                                    \n  -correspondant à __courte_description__ \n"
                                               
        self.notions.text = "Plus précisément, ce laboratoire permet de mettre en pratique les notions de: \
                            \n-__notion_1__ \
                            \n-__notion_n__ \n"
        
        self.abstraction.text = "Un effort d'abstraction a été fait pour ces points: \
                                \n-__point_1__ \
                                \n-__point_n__ \n"
        
        self.most_complex.text = "Finalement, l'ensemble de données le plus complexe que nous avons été capable de résoudre est: \
                                \n-__nom_de_l_ensemble_de_données__"
        
        
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