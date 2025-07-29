-- Conecte-se ao banco de dados 'jatoba' antes de executar este script no SQL Workbench.

-- Tabela Fabricantes
CREATE TABLE fabricantes (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único sequencial do fabricante.',
  name VARCHAR(255) NOT NULL UNIQUE COMMENT 'Nome do fabricante, deve ser único.',
  logo_url TEXT COMMENT 'URL para o logotipo do fabricante.',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data e hora de criação do registro do fabricante.',
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Última data e hora de atualização do registro do fabricante.'
);

-- Tabela equipamentos
CREATE TABLE equipamentos (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único sequencial do equipamento.',
  name VARCHAR(255) NOT NULL COMMENT 'Nome do equipamento.',
  model VARCHAR(255) NOT NULL COMMENT 'Modelo específico do equipamento.',
  manufacturer_id INT COMMENT 'ID do fabricante associado a este equipamento (sem chave estrangeira).',
  image_url TEXT COMMENT 'URL para uma imagem do equipamento.',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data e hora de criação do registro do equipamento.',
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Última data e hora de atualização do registro do equipamento.',
  UNIQUE(name, model, manufacturer_id)
);

-- Tabela Arquivos
CREATE TABLE arquivos (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único sequencial do arquivo.',
  name VARCHAR(255) NOT NULL COMMENT 'Nome do arquivo.',
  type VARCHAR(50) NOT NULL COMMENT 'Tipo do arquivo (firmware ou document).', -- CLÁUSULA CHECK REMOVIDA AQUI
  equipment_id INT COMMENT 'ID do equipamento ao qual este arquivo está associado (sem chave estrangeira).',
  file_url TEXT NOT NULL COMMENT 'URL para o local de armazenamento do arquivo.',
  file_size BIGINT NOT NULL DEFAULT 0 COMMENT 'Tamanho do arquivo em bytes.',
  download_count INT NOT NULL DEFAULT 0 COMMENT 'Número de vezes que o arquivo foi baixado.',
  uploaded_by INT COMMENT 'ID do usuário que fez o upload do arquivo (sem chave estrangeira).',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data e hora de upload do arquivo.',
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Última data e hora de atualização do registro do arquivo.'
);

-- Inserindo dados na tabela fabricantes
INSERT INTO fabricantes (name, logo_url) VALUES
('TechCorp S.A.', 'https://example.com/logos/techcorp.png'),
('Global Mfr. Ltda.', 'https://example.com/logos/global.png'),
('InnoMech Ind.', 'https://example.com/logos/innomech.png');

-- Inserindo dados na tabela equipamentos
-- Usamos IDs de fabricantes que sabemos que existirão (1, 2, 3)
INSERT INTO equipamentos (name, model, manufacturer_id, image_url) VALUES
('Processador Quantum', 'Q-9000', 1, 'https://example.com/images/q9000.jpg'),
('Sensor Ambiental', 'EnviroSense X', 2, 'https://example.com/images/esx.jpg'),
('Robô de Montagem', 'AssembleBot A1', 3, 'https://example.com/images/aba1.jpg');

-- Inserindo dados na tabela arquivos
-- Usamos IDs de equipamentos que sabemos que existirão (1, 2, 3)
INSERT INTO arquivos (name, type, equipment_id, file_url, file_size, download_count, uploaded_by) VALUES
('Firmware Q9K v1.2', 'firmware', 1, 'https://example.com/files/fw_q9k_v1.2.bin', 1024000, 50, NULL), -- uploaded_by NULL como exemplo
('Manual EnviroSense X', 'document', 2, 'https://example.com/files/manual_esx.pdf', 2048000, 120, NULL),
('Diagrama AssembleBot A1', 'document', 3, 'https://example.com/files/diag_aba1.pdf', 512000, 30, NULL);