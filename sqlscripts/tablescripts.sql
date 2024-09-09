INSERT INTO classes (nome, descricao) VALUES 
('Guerreiro', 'Especialista em combate corpo a corpo, com alta defesa e ataque físico.'),
('Mago', 'Mestre dos elementos e da magia, com alto poder de ataque mágico.'),
('Arqueiro', 'Habilidoso com arcos, excelente em combate à distância.'),
('Sacerdote', 'Utiliza bênçãos e as sombras para combate'),
('Druida', 'Muda de formas e usa a natureza para combate');

INSERT INTO habilidades (nome, tipo, classe_id) VALUES 
('Golpe de Escudo', 'rock', 1),
('Arremessar Espada', 'paper', 1),
('Corte Profudo', 'scissors', 1),
('Raio de Gelo', 'rock', 2),
('Explosão Arcana', 'paper', 2),
('Bola de Fogo', 'scissors', 2),
('Flecha Explosiva', 'rock', 3),
('Adagas Ocultas', 'paper', 3),
('Saraivada', 'scissors', 3),
('Açoite Mental', 'rock', 4),
('Fogo Divino', 'paper', 4),
('Penitência', 'scissors', 4),
('Rugido de Urso', 'rock', 5),
('Fogo Lunar', 'paper', 5),
('Garras', 'scissors', 5);



INSERT INTO npcs (nome, tipo, localizacao) VALUES 
('Rei Eldor', 'Rei', 'Boralus'),
('Ferreiro Borin', 'Ferreiro', 'Dragões'),
('Maga Seraphine', 'Maga', 'Castelo Assombrado'),
('Grommash', 'Guerreiro', 'Coliseu'),
('Ladrão Airus', 'Ladino', 'O Mercado');


INSERT INTO Missoes (nome, descricao, recompensa, cidade, opcao_sucesso, opcao_falha, personagem_id)
VALUES 
('Derrotar o Dragão', 'Você deve enfrentar o dragão que aterroriza a vila.', 500, 'Vila do Dragão',
'Usar as pedras para se proteger do fogo', 'Se esconder do fogo atrás das árvores', 1),
('Salvar a Princesa', 'Resgate a princesa do castelo assombrado.', 300, 'Castelo Assombrado',
'Invadir a masmorra pela passagem secreta', 'Tentar entrar pela porta da frente', 2);
-- IDs de personagem utilizados apenas pra simulação visto que o personagem cria a missão dentro do jogo


INSERT INTO lojas (nome, tipo_item) VALUES 
('Magia sem Fim', 'Cajado'),
('Ferraria do Anão', 'Espada'),
('Flechas Firmes', 'Arco'),
('Bênção Elemental', 'Talismã'),
('Lembrancas da Velha', 'Amuleto');

INSERT INTO equipamentos (nome, tipo, poder) VALUES 
('Espada Longa', 'Espada', 3),
('Cajado Arcano', 'Cajado', 4),
('Arco Padrão', 'Arco', 2),
('Claymore', 'Espada', 4),
('Vareta', 'Cajado', 2),
('Arco Recurvo', 'Arco', 4),
('Espada de Madeira', 'Espada', 2),
('Arco Reto', 'Arco', 3),
('Varinha Mágica', 'Cajado', 3),
('Colar de Pedras', 'Talismã', 2),
('Colar Elemental', 'Talismã', 4),
('Colar Abençoado', 'Talismã', 3),
('Trevo de 4 Folhas', 'Amuleto', 2),
('Moeda da Sorte', 'Amuleto', 4),
('Pérola', 'Amuleto', 3);

INSERT INTO Missoes (nome, descricao, recompensa, cidade, opcao_sucesso, opcao_falha, personagem_id)
VALUES 
('Destronar o Rei Corrupto', 'Assassinar o Rei que aterroriza a cidade', 600, 'Boralus',
'Trabalhar como cozinheiro e envenenar a comida do rei', 'Tentar escalar o castelo do rei e entrar pela janela', 2),
('Pescar Para os Mercadores', 'Ajude os mercadores com a pesca.', 100, 'Boralus',
'Procurar a isca certa para o peixe valioso', 'Pescar com Rede', 3),
('Derrotar a Bruxa', 'Vencer a bruxa que assombra o castelo', 400, 'Castelo Assombrado',
'Se fingir de andarilho perdido e infiltrar a casa da bruxa', 'Tentar uma armadilha com a entrega de um caldeirão novo', 1);

WITH excluded_inventory AS (
    SELECT item_id FROM inventario
)
INSERT INTO estoque (loja_id, item_id, preço)
SELECT l.id, e.id, CASE e.poder
                          WHEN 2 THEN 20
                          WHEN 3 THEN 30
                          WHEN 4 THEN 40
                       END
FROM equipamentos e
JOIN lojas l ON e.tipo = l.tipo_item
WHERE e.id NOT IN (SELECT item_id FROM excluded_inventory); -- Insere os itens dos equipamentos que não estão no inventário no estoque



-- IDs de personagem utilizados apenas pra simulação visto que o personagem cria a missão dentro do jogo


--A Tabela Duelos foi plenamente preenchida de dentro do próprio jogo, registrando os duelos feitos.

--A Tabela Inventário foi plenamente preenchida de dentro do próprio jogo, registrando os equipamentos adquiridos por cada personagem.
