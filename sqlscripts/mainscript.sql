CREATE TABLE Classes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT
);


CREATE TABLE habilidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    class_id INTEGER NOT NULL REFERENCES classes(id)
);


CREATE TABLE Personagens (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    classe_id INT,
    nivel INT,
    experiencia INT,
    FOREIGN KEY (classe_id) REFERENCES Classes(id)
);


CREATE TABLE Equipamentos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(20),
    poder INT
);

CREATE TABLE Inventario (
    id SERIAL PRIMARY KEY,
    personagem_id INT,
    quantidade INT,
    nome_equipamento VARCHAR(50)
    FOREIGN KEY (personagem_id) REFERENCES Personagens(id)
);


CREATE TABLE Missoes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    recompensa INT
);


CREATE TABLE NPCs (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(20),
    localizacao VARCHAR(100)
);


CREATE TABLE lojas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo_item VARCHAR(50) NOT NULL
);



CREATE TABLE Duelos (
    id SERIAL PRIMARY KEY,
    personagem_id INT,
    npc_id INT,
    resultado VARCHAR(10),
    experiencia_ganha INT,
    ouro_ganho INT,
    FOREIGN KEY (personagem_id) REFERENCES Personagens(id),
    FOREIGN KEY (npc_id) REFERENCES NPCs(id)
);

ALTER TABLE Missoes ADD cidade VARCHAR(100);

ALTER TABLE Missões ADD COLUMN opcao_sucesso TEXT, ADD COLUMN opcao_falha TEXT;

ALTER TABLE inventario
ADD CONSTRAINT unique_personagem_equipamento UNIQUE (personagem_id, nome_equipamento);

CREATE TABLE estoque (
    id SERIAL PRIMARY KEY,
    loja_id INT REFERENCES lojas(id) ON DELETE CASCADE,
    item_id INT REFERENCES equipamentos(id) ON DELETE CASCADE,
    preço INT NOT NULL
);

ALTER TABLE missoes ADD COLUMN personagem_id INT;

ALTER TABLE classes ADD COLUMN icone_classe BYTEA;

CREATE VIEW vw_personagem_duelos AS
SELECT
    p.nome AS personagem,
    n.nome AS npc,
    d.resultado,
    d.personagem_id
FROM
    Duelos d
INNER JOIN Personagens p ON d.personagem_id = p.id
INNER JOIN NPCs n ON d.npc_id = n.id;

CREATE PROCEDURE proc_criar_npc(IN nome VARCHAR(50), IN tipo VARCHAR(20), IN localizacao VARCHAR(100))
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO NPCs (nome, tipo, localizacao) VALUES (nome, tipo, localizacao);
END;
$$;