PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Tabela: user
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: transacao
CREATE TABLE IF NOT EXISTS transacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'saída')),
    descricao TEXT,
    data_transacao DATE NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_transacao_user ON transacao(user_id);
CREATE INDEX IF NOT EXISTS idx_transacao_data ON transacao(data_transacao);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;