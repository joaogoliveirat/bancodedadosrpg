import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="rpg",
            user="postgres",
            password="2019memes13",
            host="localhost"
        )
        self.cursor = self.conn.cursor()
        

    def fetch_all_classes(self):
        self.cursor.execute("SELECT id, nome FROM classes")
        return self.cursor.fetchall()

    def create_personagem(self, nome, classe_id):
        self.cursor.execute(
            "INSERT INTO personagens (nome, classe_id, nivel, experiencia) VALUES (%s, %s, 1, 0)",
            (nome, classe_id)
        )
        self.conn.commit()

    def fetch_all_personagens(self):
        self.cursor.execute("SELECT id, nome FROM personagens")
        return self.cursor.fetchall()

    def fetch_personagem_by_id(self, personagem_id):
        self.cursor.execute("SELECT * FROM personagens WHERE id = %s", (personagem_id,))
        return self.cursor.fetchone()
    
    def fetch_missions_by_city(self, cidade):

        self.cursor.execute("""
        SELECT id, nome, descricao, recompensa, opcao_sucesso, opcao_falha 
        FROM Missoes 
        WHERE cidade = %s
    """, (cidade,))
        missoes = self.cursor.fetchall()

        return missoes
    
    def update_personagem_xp_nivel(self, personagem_id, xp, nivel):
        self.cursor.execute(
            "UPDATE Personagens SET experiencia = %s, nivel = %s WHERE id = %s",
            (xp, nivel, personagem_id)
        )
    def get_mission_reward(self, missao_id):

        self.cursor.execute("SELECT recompensa FROM Missoes WHERE id = %s", (missao_id,))
        recompensa = self.cursor.fetchone()
        return recompensa[0] if recompensa else 0

    def update_character_experience(self, character_id, experiencia):

        self.cursor.execute("""
        SELECT experiencia, nivel FROM Personagens WHERE id = %s;
        """, (character_id,))
        result = self.cursor.fetchone()
        
        if result:
            exp_atual, nivel_atual = result

            exp_nova = exp_atual + experiencia

            if exp_nova >= 300:
                novo_nivel = nivel_atual + exp_nova // 300
                exp_nova = exp_nova % 300  
            else:
                novo_nivel = nivel_atual

            self.cursor.execute("""
            UPDATE Personagens SET experiencia = %s, nivel = %s WHERE id = %s;
            """, (exp_nova, novo_nivel, character_id))
            self.conn.commit()
        else:

            print(f"Erro ao adicionar item")
    
    

    def fetch_character(self, personagem_id):

        self.cursor.execute("SELECT id, nome, classe_id, nivel, experiencia FROM Personagens WHERE id = %s", (personagem_id,))
        character = self.cursor.fetchone()

        return character
    
    def update_mission_creation(self, nome, descricao, recompensa, opcao_sucesso, opcao_falha, cidade, personagem_id):
        try:

            self.cursor.execute("""
                INSERT INTO Missoes (nome, descricao, recompensa, opcao_sucesso, opcao_falha, cidade, personagem_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nome, descricao, recompensa, opcao_sucesso, opcao_falha, cidade, personagem_id))
            self.conn.commit()

        except Exception as e:
            print(f"Erro ao criar missão: {e}")

    def add_item_to_character(self, character_id, item_name, quantidade):
        try:
            self.cursor.execute("SELECT COALESCE(MAX(id), 0) FROM equipamentos")

            self.cursor.execute("""
                    INSERT INTO inventario (personagem_id, quantidade, nome_equipamento)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (personagem_id, nome_equipamento) DO UPDATE
                    SET quantidade = inventario.quantidade + EXCLUDED.quantidade;
            """, (character_id, quantidade, item_name))
            

            
            self.conn.commit()

        except Exception as e:
            print(f"Erro ao adicionar item: {e}")

    def add_item_to_equip(self, item_name, item_type, item_power,):
        try:
         
            self.cursor.execute("""
                        INSERT INTO equipamentos (nome, tipo, poder)
                        VALUES ( %s, %s, %s)
                    """, ( item_name, item_type, item_power))

            self.conn.commit()

        except Exception as e:
            print(f"Erro ao adicionar item: {e}")
    
    def get_class_abilities(self, character_class_id):
        try:
            self.cursor.execute("""
                SELECT nome, tipo
                FROM habilidades
                WHERE classe_id = %s
            """, (character_class_id,))
            abilities = self.cursor.fetchall()

            class_abilities = {}
            for ability in abilities:
                nome, tipo = ability
                class_abilities[tipo] = nome

            return class_abilities

        except Exception as e:
            print(f"Erro ao buscar habilidades: {e}")
            return {}
    def get_stores(self):
        try:
            self.cursor.execute("""
                SELECT id, nome, tipo_item 
                FROM lojas 
            """)
            stores = self.cursor.fetchall()

            store_list = []
            for store in stores:
                store_id, store_name, tipo = store
                store_list.append({'id': store_id, 'nome': store_name, 'tipo_item': tipo})

            return store_list

        except Exception as e:
            print(f"Erro ao buscar lojas: {e}")
            return []



    def fetch_random_npc(self):
        try:
            self.cursor.execute("SELECT * FROM NPCs ORDER BY RANDOM() LIMIT 1")
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar NPC: {e}")
            return None
        
    def record_duel(self, character_id, npc_id, result, experience_gained, gold_gained):
        try:
            self.cursor.execute("""
                INSERT INTO Duelos (personagem_id, npc_id, resultado, experiencia_ganha, ouro_ganho)
                VALUES (%s, %s, %s, %s, %s)
            """, (character_id, npc_id, result, experience_gained, gold_gained))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao registrar o duelo: {e}")

    def get_gold_coins(self, character_id):
        try:
            self.cursor.execute("""
                SELECT quantidade 
                FROM inventario
                WHERE personagem_id = %s AND nome_equipamento = 'Gold Coin'
            """, (character_id,))
            result = self.cursor.fetchone()

            if result:
                return result[0]
            else:
                return 0  

        except Exception as e:
            print(f"Erro ao buscar Gold Coins: {e}")
            return 0
    def subtract_gold_coins(self, character_id, amount):
        try:
            self.cursor.execute("""
                SELECT quantidade 
                FROM inventario 
                WHERE personagem_id = %s AND nome_equipamento = 'Gold Coin'
            """, (character_id,))
            
            result = self.cursor.fetchone()
            
            if result and result[0] >= amount:
                self.cursor.execute("""
                    UPDATE inventario 
                    SET quantidade = quantidade - %s 
                    WHERE personagem_id = %s AND nome_equipamento = 'Gold Coin'
                """, (amount, character_id))
                self.conn.commit()
                return True
            else:
                print("Nao há Gold Coins Suficientes.")
                return False
            
        except Exception as e:
            print(f"Erro ao calcular os Gold Coins: {e}")
            return False
    def get_available_items(self, store_id, character_class_id):
        try:
            self.cursor.execute("""
                SELECT tipo_item
                FROM lojas
                WHERE id = %s
            """, (store_id,))
            
            store_type = self.cursor.fetchone()[0]

            allowed_item_types = []
            if character_class_id == 1: 
                allowed_item_types = ['Espada', 'Talismã', 'Amuleto']
            elif character_class_id == 2: 
                allowed_item_types = ['Cajado', 'Talismã', 'Amuleto']
            elif character_class_id == 3:
                allowed_item_types = ['Arco', 'Talismã', 'Amuleto']
            elif character_class_id == 4:
                allowed_item_types = ['Cajado', 'Talismã', 'Amuleto']
            elif character_class_id == 5:
                allowed_item_types = ['Espada', 'Cajado', 'Talismã', 'Amuleto']

            if store_type in allowed_item_types:
                self.cursor.execute("""
                    SELECT e.nome, e.poder, es.preço
                    FROM estoque es
                    JOIN equipamentos e ON es.item_id = e.id
                    WHERE es.loja_id = %s AND e.tipo = %s
                """, (store_id, store_type))
                
                available_items = self.cursor.fetchall()

                items = []
                for item in available_items:
                    nome, poder, preço = item
                    items.append({
                        'nome': nome,
                        'poder': poder,
                        'preço': preço,
                    })

                return items

            else:
                print("Essa classe não pode comprar desta loja.")
                return []

        except Exception as e:
            print(f"Erro pegando itens disponiveis: {e}")
            return []

    def get_character_info(self, character_id):
        query = "SELECT nome, nivel, experiencia FROM personagens WHERE id = %s"
        self.cursor.execute(query, (character_id,))
        return self.cursor.fetchone()

    def get_character_inventory(self, character_id):
        query = "SELECT nome_equipamento, quantidade FROM inventario WHERE personagem_id = %s"
        self.cursor.execute(query, (character_id,))
        return self.cursor.fetchall()
    
    def get_equipment(self):
        query = "SELECT nome, poder FROM equipamentos"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def remove_mission(self, missao_id):
        try:
            self.cursor.execute("DELETE FROM Missoes WHERE id = %s", (missao_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao remover missão: {e}")

    def insert_class_icon(self, id, icone_path):
        try:
            with open(icone_path, "rb") as file:
                binary_data = file.read()

            query = """
            UPDATE classes
            SET icone_classe = %s
            WHERE id = %s;
            """
            self.cursor.execute(query, (binary_data, id))
            self.conn.commit()

        except Exception as e:
            print(f"Erro ao inserir icone: {e}")

    def get_class_icon(self, id):
        try:
            query = "SELECT icone_classe FROM classes WHERE id = %s"
            self.cursor.execute(query, (id,))
            icon_data = self.cursor.fetchone()[0]

            return icon_data

        except Exception as e:
            print(f"Erro ao pegar icone: {e}")
            return None
        
    def check_duels(self, id):
        self.cursor.execute("SELECT * FROM vw_personagem_duelos WHERE personagem_id = %s", (id,))
        rows = self.cursor.fetchall()
        return rows
    
    def create_npc(self, nome, tipo, localizacao):
        self.cursor.execute("CALL proc_criar_npc(%s, %s, %s)", (nome, tipo, localizacao))
        self.conn.commit()

        

    def close(self):
        self.cursor.close()
        self.conn.close()
