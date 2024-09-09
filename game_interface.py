from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from database import Database
import random


class RPGGame(QMainWindow):
    def __init__(self, personagem):
        super().__init__()
        db = Database()
        self.personagem = personagem
        self.character_id = personagem[0]
        self.personagem_nome = personagem[1]
        self.setWindowTitle(f'RPG de Texto - Jogando com {self.personagem[1]}')
        self.setGeometry(200, 200, 800, 600)
        self.current_city = None
        self.character_class = personagem[2]
        self.class_abilities = db.get_class_abilities(self.character_class)
        db.insert_class_icon(1, "assets/guerreiroicon.png")
        db.insert_class_icon(2, "assets/magoicon.png")
        db.insert_class_icon(3, "assets/archersymbol.png")
        db.insert_class_icon(4, "assets/priesticon.png")
        db.insert_class_icon(5, "assets/druidicon.png")
        class_icon_data = db.get_class_icon(self.character_class)
 
    
        
        main_layout = QVBoxLayout()
        
     
        self.map_label = QLabel(self)
        pixmap = QPixmap('assets/hoenn.png')
        self.map_label.setPixmap(pixmap)
        self.map_label.mousePressEvent = self.map_clicked
        pixmap.loadFromData(class_icon_data)
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setGeometry(10, 10, pixmap.width(), pixmap.height())
        
    
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        
        main_layout.addWidget(self.map_label)
        main_layout.addWidget(self.text_area)
        main_layout.addWidget(self.icon_label)

        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        
        self.load_initial_story()  

    
        
    
    def load_initial_story(self):
        self.text_area.append("Bem-vindo ao mundo de RPG! Selecione uma cidade no mapa para começar sua aventura.")

    def map_clicked(self, event):
        
        position = event.pos()
        city = self.detect_city(position)
        if city:
            self.current_city = city
            self.load_city_missions(city)

    def detect_city(self, position):
        city_map = {
            'Vila do Dragão': (576, 110, 640, 200),
            'Castelo Assombrado': (190, 130, 270, 190),
            'Coliseu': (200, 364, 260, 400),
            'O Mercado': (493, 357, 550, 400),
            'Boralus':(356, 249, 415, 300),
            'Bag':(682,331,730,390)
        }
        
        for city_name, (x1, y1, x2, y2) in city_map.items():
            if x1 <= position.x() <= x2 and y1 <= position.y() <= y2:
                return city_name
            
        return None
    
   



    def load_city_missions(self, city_name):
        db = Database()
        missões = db.fetch_missions_by_city(city_name)
        
        self.text_area.clear()

        if city_name.lower() == "coliseu":
            self.text_area.append("Você está no Coliseu! Pronto para um duelo?")
            duel_button = QPushButton("Iniciar Duelo", self)
            duel_button.clicked.connect(self.start_duel)
            button_layout = QHBoxLayout()
            button_layout.addWidget(duel_button)
            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            history_button = QPushButton("Histórico", self)
            history_button.clicked.connect(self.duel_history)
            button_layout.addWidget(history_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.layout().addWidget(button_widget)

        elif city_name.lower() == 'o mercado':
            self.text_area.append("Bem Vindo ao Mercado! O Que quer comprar?")
            market_button = QPushButton("Entrar no Mercado", self)
            market_button.clicked.connect(self.enter_market)
            button_layout = QHBoxLayout()
            button_layout.addWidget(market_button)
            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.layout().addWidget(button_widget)
        elif city_name.lower() == 'bag':
            market_button = QPushButton("Inventário", self)
            market_button.clicked.connect(self.show_character_status)
            button_layout = QHBoxLayout()
            button_layout.addWidget(market_button)
            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.layout().addWidget(button_widget)


        else:
            self.text_area.append(f"Você chegou em {city_name}. Missões disponíveis:")

            mission_layout = QVBoxLayout()

            for missão in missões:
                missao_id, nome, descricao, recompensa, opcao_sucesso, opcao_falha = missão
                
                btn_missao = QPushButton(f'{nome}: {descricao}', self)
                
                btn_missao.clicked.connect(lambda _, m_id=missao_id, nome=nome, desc=descricao, recomp=recompensa, opsuc=opcao_sucesso, opfal=opcao_falha: self.show_mission_choices(m_id, nome, desc, recomp, opsuc, opfal))
                
                mission_layout.addWidget(btn_missao)

            btn_create_mission = QPushButton("Criar Missão", self)
            btn_create_mission.clicked.connect(lambda: self.create_mission(city_name))
            mission_layout.addWidget(btn_create_mission)
            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            mission_layout.addWidget(back_button)

            mission_widget = QWidget()
            mission_widget.setLayout(mission_layout)
            self.layout().addWidget(mission_widget)

            


    def create_mission(self, city_name):
        
        nome, ok1 = QInputDialog.getText(self, 'Criar Missão', 'Nome da missão:')
        descricao, ok2 = QInputDialog.getText(self, 'Criar Missão', 'Descrição:')
        recompensa, ok3 = QInputDialog.getInt(self, 'Criar Missão', 'Recompensa (XP):')
        opcao_sucesso, ok4 = QInputDialog.getText(self, 'Criar Missão', 'Opção de sucesso:')
        opcao_falha, ok5 = QInputDialog.getText(self, 'Criar Missão', 'Opção de falha:')
        
        if ok1 and ok2 and ok3 and ok4 and ok5:
            db = Database()
            db.update_mission_creation(nome, descricao, recompensa, opcao_sucesso, opcao_falha, city_name, self.character_id)
            self.text_area.append("Missão criada com sucesso!")  

        button_layout = QHBoxLayout()
        back_button = QPushButton("Voltar", self)
        back_button.clicked.connect(self.main_screen)
        button_layout.addWidget(back_button)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        self.layout().addWidget(button_widget)




    def show_mission_choices(self, missao_id, nome, descricao, recompensa, opcao_sucesso, opcao_falha):
        self.text_area.clear()
        self.text_area.append(f"Missão: {nome}")
        self.text_area.append(descricao)
        
        btn_success = QPushButton(opcao_sucesso, self)
        btn_success.clicked.connect(lambda _, m_id=missao_id: self.complete_mission(m_id, True))
        
        btn_failure = QPushButton(opcao_falha, self)
        btn_failure.clicked.connect(lambda _, m_id=missao_id: self.complete_mission(m_id, False))
        button_layout = QHBoxLayout()
        
        button_layout.addWidget(btn_success)
        button_layout.addWidget(btn_failure)
        back_button = QPushButton("Voltar", self)
        back_button.clicked.connect(self.main_screen)
        button_layout.addWidget(back_button)
        
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        
        self.layout().addWidget(button_widget)

    
    def complete_mission(self, missao_id, sucesso):
        db = Database()
        
        if sucesso:
            recompensa = db.get_mission_reward(missao_id)
            print(f"Recompensa obtida: {recompensa} XP")  # Debugging
            db.update_character_experience(self.character_id, recompensa)
            db.remove_mission(missao_id)
            self.text_area.append(f"Missão completada com sucesso! Você ganhou {recompensa} XP.")
            self.award_random_item()
            

        else:
            self.text_area.append("Missão falhou, tente novamente.")


 
        self.update_character_status()
        button_layout = QHBoxLayout()
        back_button = QPushButton("Voltar", self)
        back_button.clicked.connect(self.main_screen)
        button_layout.addWidget(back_button)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        self.layout().addWidget(button_widget)

    def update_character_status(self):
        db = Database()
        character = db.fetch_character(self.character_id)
        nivel, experiencia = character[3], character[4]
    
        self.text_area.append(f"Status do personagem: Nível {nivel}, Experiência {experiencia}")
    
    def gain_experience(self, xp_ganho):
        db = Database()
        current_xp = self.personagem[3] + xp_ganho
        new_level = self.personagem[2] + (current_xp // 300)
        current_xp = current_xp % 300 
        
        db.update_personagem_xp_nivel(self.personagem[0], current_xp, new_level)
        
        self.personagem = (self.personagem[0], self.personagem[1], new_level, current_xp)
        self.text_area.append(f"Parabéns! Você agora está no nível {new_level} com {current_xp} XP restantes.")




    def award_random_item(self):
        db = Database()
        items = ["Berloque", "Talismã", "Máscara", "Anel", "Amuleto"]
        item_type = random.choice(items)
        item_power = random.randint(1, 5)
        quantidade = 1
        equiplist = db.get_equipment()
        repeat = False
        
        item_name, ok = QInputDialog.getText(self, 'Nome do Item', f'Você encontrou um {item_type}! Dê um nome ao seu item:')
        
        if ok:
            for equip in equiplist:
                if item_name in equip[0]:
                    repeat = True
        if repeat == False: 
            db.add_item_to_character(self.character_id, item_name, quantidade)
            db.add_item_to_equip(item_name, item_type, item_power)
            self.text_area.append(f"Você ganhou {item_name} com {item_power} de poder!")
        if repeat == True:
            self.text_area.append("Ja existe um item com este nome, escolha outro nome.")
            item_name, ok = QInputDialog.getText(self, 'Nome do Item', f'Você encontrou um {item_type}! Dê um nome ao seu item:')
            db.add_item_to_character(self.character_id, item_name, quantidade)
            db.add_item_to_equip(item_name, item_type, item_power)
            self.text_area.append(f"Você ganhou {item_name} com {item_power} de poder!")

    def start_duel(self):
        self.current_health = 100
        self.npc_health = 100
        npc = self.get_random_npc()
        self.show_duel_options(npc)


        
    def get_random_npc(self):
        db = Database()
        return db.fetch_random_npc()
    
    def show_duel_options(self, npc):
        self.text_area.clear()
        npc_name = npc[1]
        self.text_area.append(f"Você está duelando contra {npc_name}!")

        btn_rock = QPushButton(f'({self.class_abilities["rock"]})', self)
        btn_rock.clicked.connect(lambda: self.player_move('rock', npc))

        btn_paper = QPushButton(f'({self.class_abilities["paper"]})', self)
        btn_paper.clicked.connect(lambda: self.player_move('paper', npc))

        btn_scissors = QPushButton(f'({self.class_abilities["scissors"]})', self)
        btn_scissors.clicked.connect(lambda: self.player_move('scissors', npc))
        button_layout = QHBoxLayout()

        button_layout.addWidget(btn_rock)
        button_layout.addWidget(btn_paper)
        button_layout.addWidget(btn_scissors)
        

        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        
        self.layout().addWidget(button_widget)

    def player_move(self, move_type, npc):
        npc_move = random.choice(['rock', 'paper', 'scissors'])
        self.text_area.append(f"Você usou {self.class_abilities[move_type]}!")
        self.text_area.append(f"O NPC tentou golpear de volta!")
        button_layout = QHBoxLayout()

        if move_type == npc_move:
            self.text_area.append("Empate!")
        elif (move_type == 'rock' and npc_move == 'scissors') or \
             (move_type == 'paper' and npc_move == 'rock') or \
             (move_type == 'scissors' and npc_move == 'paper'):
            self.npc_health -= 20  
            self.text_area.append("Você venceu esta rodada!")
        else:
            self.current_health -= 20  
            self.text_area.append("Você perdeu esta rodada!")

        if self.current_health <= 0:
            self.text_area.append("Você perdeu o duelo!")
            self.end_duel(npc)
            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
        
            self.layout().addWidget(button_widget)

        elif self.npc_health <= 0:
            self.text_area.append("Você venceu o duelo!")
            self.end_duel(npc)
            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
        
            self.layout().addWidget(button_widget)

    def end_duel(self, npc):
        db = Database()
        if self.current_health > 0:
            experience_gained = 100
            quantidade = random.randint(10, 50)
            db.add_item_to_character(self.character_id, "Gold Coin", quantidade)
            db.update_character_experience(self.character_id, experience_gained)
            db.record_duel(self.character_id, npc[0], "vitoria" if self.current_health > 0 else "derrota", experience_gained, quantidade)
        else:
            experience_gained = 0
            quantidade = 0
            db.record_duel(self.character_id, npc[0], "vitoria" if self.current_health > 0 else "derrota", experience_gained, quantidade)



    def enter_market(self):
        try:
            db = Database()
            stores = db.get_stores()


            if not stores:
                self.text_area.append("Sem lojas no mercado.")
                return


            self.text_area.append("Escolha uma loja para entrar:")

            button_layout = QVBoxLayout()
            

            for store in stores:
                store_button = QPushButton(store['nome'], self)
                store_button.setFixedSize(130, 60)
                store_button.clicked.connect(lambda _, s=store: self.enter_store(s))
                button_layout.addWidget(store_button)

            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
        
            self.layout().addWidget(button_widget)
            

        except Exception as e:
            print(f"Erro ao entrar no mercado: {e}")





    def enter_store(self, store):
        try:
            db = Database()
            self.text_area.clear()
            self.text_area.append(f"Voce entrou em {store['nome']}.")

            available_items = db.get_available_items(store['id'], self.character_class)


            if not available_items:
                self.text_area.append("Nao ha itens disponiveis.")
                return

            self.text_area.append("Itens disponiveis para compra:")

            for i in reversed(range(self.layout().count())): 
                widget = self.layout().itemAt(i).widget()
                if widget is not None: 
                    widget.deleteLater()

            button_layout = QHBoxLayout()

            for item in available_items:
                item_button = QPushButton(f"{item['nome']} - {item['preço']} Gold Coins", self)
                item_button.setFixedSize(190, 50)
                item_button.clicked.connect(lambda _, i=item: self.attempt_purchase(i))
                button_layout.addWidget(item_button)

            back_button = QPushButton("Voltar", self)
            back_button.clicked.connect(self.main_screen)
            button_layout.addWidget(back_button)
            button_widget = QWidget()
            button_widget.setLayout(button_layout)
        
            self.layout().addWidget(button_widget)

        except Exception as e:
            print(f"Erro ao entrar na loja: {e}")




    def attempt_purchase(self, item):
        db = Database()
        gold_coins = db.get_gold_coins(self.character_id)
        
        if gold_coins >= item['preço']:
            self.purchase_item(item)
        else:
            self.text_area.append("Voce nao tem Gold Coins suficientes para comprar esse item.")

    def purchase_item(self, item):
        db = Database()

        db.subtract_gold_coins(self.character_id, item['preço'])
        

        db.add_item_to_character(self.character_id, item['nome'], 1)
        
        self.text_area.append(f"Voce comprou {item['nome']}!")


    def main_screen(self):
        db = Database()
        class_icon_data = db.get_class_icon(self.character_class)
        main_layout = QVBoxLayout()
        
        self.map_label = QLabel(self)
        pixmap = QPixmap('assets/hoenn.png')
        self.map_label.setPixmap(pixmap)
        self.map_label.mousePressEvent = self.map_clicked
        pixmap.loadFromData(class_icon_data)
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setGeometry(10, 10, pixmap.width(), pixmap.height())
        
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        
        main_layout.addWidget(self.map_label)
        main_layout.addWidget(self.text_area)
        main_layout.addWidget(self.icon_label)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.text_area.append("Bem-vindo ao mundo de RPG de Banco de Dados! Clique em uma cidade no mapa para continuar sua aventura.")


    def show_character_status(self):

        db = Database()

  
        character_info = db.get_character_info(self.character_id)
        inventory = db.get_character_inventory(self.character_id)
        equiplist = db.get_equipment()


        total_power = 0
        for equip in equiplist:
            for item in inventory:
                if equip[0] in item[0]:
                    total_power = total_power + (equip[1]*item[1])



        self.text_area.clear()
        self.text_area.append(f"Personagem: {character_info[0]}")
        self.text_area.append(f"Level: {character_info[1]}")
        self.text_area.append(f"EXP: {character_info[2]}")
        self.text_area.append(f"Poder total dos itens: {total_power}")

        self.text_area.append("\nInventory:")
        if not inventory:
            self.text_area.append("Seu inventário está vazio.")
        else:
            for item in inventory:
                for equip in equiplist:
                    if equip[0] in item[0]:
                        self.text_area.append(f"- {item[0]} (Poder: {equip[1]})")

    def duel_history(self):
        db = Database()
        historico = db.check_duels(self.character_id)
        if historico == []:
            self.text_area.clear()
            self.text_area.append("Você ainda não duelou. Inicie um duelo para registrá-lo no histórico.")
        for duelo in historico:
            self.text_area.append(f"{duelo[0]} duelou contra {duelo[1]} e o resultado foi {duelo[2]}.")

        
    def clear_layout(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout.removeItem(item)




        

    

