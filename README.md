# API Jatobá - Gerenciamento de Equipamentos, Fabricantes e Arquivos

---

## 📄 Descrição do Projeto

A API Jatobá é um backend robusto e flexível, construído com **Flask** e **PyMySQL**, projetado para gerenciar informações sobre **fabricantes**, **equipamentos** e **arquivos** (como firmwares e documentos). Ela oferece funcionalidades CRUD (Criar, Ler, Atualizar, Deletar) para essas entidades, além de recursos de busca global, upload/download de arquivos e estatísticas administrativas.

O objetivo principal desta API é fornecer uma base sólida para sistemas de gerenciamento de ativos, permitindo o registro, a organização e a recuperação eficiente de dados relacionados a hardware e seus componentes de software/documentação.

## ✨ Funcionalidades Principais

* **Gerenciamento de Fabricantes**: Adicione, liste, atualize e remova fabricantes, com suporte para upload de logos.
* **Gerenciamento de Equipamentos**: Adicione, liste, atualize e remova equipamentos, com associação a fabricantes e upload de imagens.
* **Gerenciamento de Arquivos**: Faça upload, liste, atualize metadados e gerencie downloads de firmwares e documentos, associando-os a equipamentos.
* **Funcionalidades de Busca**: Busque por fabricantes e equipamentos usando termos específicos.
* **Estatísticas Administrativas**: Obtenha insights sobre os dados armazenados na API.
* **Sistema de Logging Detalhado**: Logs configuráveis para monitoramento e depuração, salvos em arquivo e exibidos no console.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Flask**: Micro-framework web para Python.
* **PyMySQL**: Driver nativo Python para MySQL/MariaDB.
* **python-dotenv**: Para gerenciar variáveis de ambiente.

## 🚀 Como Configurar e Rodar

Siga estes passos para configurar e executar a API localmente.

### Pré-requisitos

* **Python 3.x** instalado.
* Um servidor de banco de dados **MariaDB** ou **MySQL** em execução.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/api-jatoba.git](https://github.com/seu-usuario/api-jatoba.git) # Substitua pelo seu link do repositório
cd api-jatoba
