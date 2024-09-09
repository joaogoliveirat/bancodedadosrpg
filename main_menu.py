from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QWidget, QMessageBox
from database import Database
from game_interface import RPGGame

class CreateCharacterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Criar Novo Personagem')
        self.setGeometry(150, 150, 400, 300)
        
        layout = QVBoxLayout()
        
        self.name_label = QLabel('Nome do Personagem:', self)
        layout.addWidget(self.name_label)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_input)
        
        self.class_label = QLabel('Classe do Personagem:', self)
        layout.addWidget(self.class_label)
        self.class_combo = QComboBox(self)
        self.load_classes()
        layout.addWidget(self.class_combo)

        create_btn = QPushButton('Criar', self)
        create_btn.clicked.connect(self.create_character)
        layout.addWidget(create_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def load_classes(self):
        db = Database()
        classes = db.fetch_all_classes()
        for classe in classes:
            self.class_combo.addItem(classe[1], classe[0])
    
    def create_character(self):
        nome = self.name_input.text()
        classe_id = self.class_combo.currentData()
        
        if not nome:
            QMessageBox.warning(self, 'Erro', 'Nome do personagem não pode estar vazio.')
            return
        
        db = Database()
        db.create_personagem(nome, classe_id)
        
        QMessageBox.information(self, 'Sucesso', 'Personagem criado com sucesso!')
        self.close()

class ChooseCharacterWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent 
        
        self.setWindowTitle('Escolher Personagem')
        self.setGeometry(150, 150, 400, 300)
        
        layout = QVBoxLayout()
        
        self.character_combo = QComboBox(self)
        self.load_characters()
        layout.addWidget(self.character_combo)
        
        choose_btn = QPushButton('Escolher', self)
        choose_btn.clicked.connect(self.choose_character)
        layout.addWidget(choose_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def load_characters(self):
        db = Database()
        personagens = db.fetch_all_personagens()
        for personagem in personagens:
            self.character_combo.addItem(personagem[1], personagem[0])
    
    def choose_character(self):
        personagem_id = self.character_combo.currentData()
        
        if personagem_id:
            db = Database()
            personagem = db.fetch_personagem_by_id(personagem_id)
            self.parent.start_game(personagem) 
            self.close()
        else:
            QMessageBox.warning(self, 'Erro', 'Nenhum personagem selecionado.')

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tela Inicial')
        self.setGeometry(100, 100, 400, 300)
        
        main_layout = QVBoxLayout()
        
        create_btn = QPushButton('Criar Personagem', self)
        create_btn.clicked.connect(self.open_create_character)
        main_layout.addWidget(create_btn)
        
        choose_btn = QPushButton('Escolher Personagem', self)
        choose_btn.clicked.connect(self.choose_character)
        main_layout.addWidget(choose_btn)

        create_npc_btn = QPushButton('Criar NPC', self)
        create_npc_btn.clicked.connect(self.npc_criar)
        main_layout.addWidget(create_npc_btn)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def open_create_character(self):
        self.create_window = CreateCharacterWindow()
        self.create_window.show()
    
    def choose_character(self):
        self.choose_window = ChooseCharacterWindow(self) 
        self.choose_window.show()
    
    def start_game(self, personagem):
        self.game_window = RPGGame(personagem)
        self.game_window.show()
        self.close()
    
    def npc_criar(self):
        self.npc_window = CreateNPCWindow()
        self.npc_window.show()
        
class CreateNPCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Criar Novo Personagem')
        self.setGeometry(150, 150, 400, 300)
        
        layout = QVBoxLayout()
        
        self.npc_name = QLabel('Nome do NPC:', self)
        layout.addWidget(self.npc_name)
        self.name_input = QLineEdit(self)
        layout.addWidget(self.name_input)
        
        self.tipo_npc = QLabel('Tipo do NPC:', self)
        layout.addWidget(self.tipo_npc)
        self.tipo_input = QLineEdit(self)
        layout.addWidget(self.tipo_input)

        self.loc_npc = QLabel('Localização do NPC:', self)
        layout.addWidget(self.loc_npc)
        self.loc_input = QLineEdit(self)
        layout.addWidget(self.loc_input)

        create_btn = QPushButton('Criar', self)
        create_btn.clicked.connect(self.create_npc)
        layout.addWidget(create_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_npc(self):
        db = Database()
        nome = self.name_input.text()
        tipo = self.tipo_input.text()
        localizacao = self.loc_input.text()
        db.create_npc(nome, tipo, localizacao)
        self.close()

