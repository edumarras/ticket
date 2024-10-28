-- Ativar restrições de chaves estrangeiras
PRAGMA foreign_keys = ON;

-- Criar tabela Pessoas
CREATE TABLE IF NOT EXISTS Pessoas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Login TEXT NOT NULL UNIQUE,
    Senha TEXT NOT NULL,
    ADM INTEGER NOT NULL
);

-- Inserir dados iniciais em Pessoas
INSERT INTO Pessoas (Login, Senha, ADM) VALUES
('usuario1', 'senha1', 0),
('adm1', 'senha2', 1),
('usuario2', 'senha3', 0),
('usuario3', 'senha4', 0),
('adm2', 'senha5', 1);

-- Criar tabela Ticket
CREATE TABLE IF NOT EXISTS Ticket (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Titulo TEXT NOT NULL,
    Descricao TEXT,
    Prioridade INTEGER,
    ID_pessoa INTEGER NULL,
    Status INTEGER DEFAULT 0,
    FOREIGN KEY (ID_pessoa) REFERENCES Pessoas(ID)
);

-- Inserir dados iniciais em Ticket (Status padrão 0, ID_pessoa NULL)
INSERT INTO Ticket (Titulo, Descricao, Prioridade) VALUES
('Problema no sistema', 'Descrição do problema...', 1),
('Erro de carregamento', 'Descrição do erro...', 3),
('Bug na aplicação', 'Descrição do bug...', 2),
('Falha de login', 'Usuário não consegue fazer login.', 2),
('Atualização de sistema', 'Erro durante a atualização.', 1),
('Interface travando', 'Interface gráfica congela após o login.', 2),
('Servidor indisponível', 'O servidor está fora do ar.', 3),
('Problema de segurança', 'Vulnerabilidade detectada no sistema.', 1);
