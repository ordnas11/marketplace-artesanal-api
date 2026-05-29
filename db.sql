CREATE DATABASE marketplace_artesanal;

USE marketplace_artesanal;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    status ENUM('ATIVO','INATIVO') DEFAULT 'ATIVO',

    usuario_id INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(usuario_id)
    REFERENCES usuarios(id)
    ON DELETE CASCADE
);

CREATE TABLE formas_venda (
    id INT AUTO_INCREMENT PRIMARY KEY,

    tipo ENUM(
        'UNITARIA',
        'ASSINATURA',
        'PACOTE'
    ) NOT NULL,

    condicoes_pagamento TEXT,

    produto_id INT NOT NULL,

    FOREIGN KEY(produto_id)
    REFERENCES produtos(id)
    ON DELETE CASCADE
);