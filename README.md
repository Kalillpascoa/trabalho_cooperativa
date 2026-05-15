**Sistema de Cooperativa Agrícola 🌱🚜**

Sistema web desenvolvido em Django para gerenciamento de cooperativa agrícola, permitindo o controle de produtores, clientes, produtos, pedidos e estoque.

👥 **Alunos/Desenvolvedores**

Kalill José Viana da Páscoa

Robson Ferreira dos Santos Junior

**🛠️ Pré-requisitos**

**Antes de executar o projeto, instale:**

Python 3.x
pip
virtualenv

**🚀 Instalação**

**1. Clone o repositório**
git clone https://github.com/Kalillpascoa/trabalho_cooperativa.git
cd trabalho_cooperativa-main/code

**2. Crie e ative um ambiente virtual**

É importante que o ambiente virtual seja criado na pasta que contém o arquivo manage.py.

**Linux / macOS**
python3 -m venv venv
source venv/bin/activate

**Windows (CMD / PowerShell)**
python3 -m venv venv
venv\Scripts\activate

**3. Instale as dependências**
pip install django

**4. Execute as migrations**
python3 manage.py migrate

**5. Crie um superusuário**
python3 manage.py createsuperuser

Preencha:
Usuário: admin
Senha: admin

**▶️ Como executar**
Rodar o servidor de desenvolvimento
python3 manage.py runserver

O sistema ficará disponível em:
http://127.0.0.1:8000/

**📋 Funcionalidades do Sistema**

✅ Cadastro de usuários
✅ Login e logout
✅ Controle de produtores
✅ Controle de clientes
✅ Cadastro de produtos
✅ Controle de estoque
✅ Cadastro de pedidos
✅ Dashboard de estoque
✅ Gráficos de produtos e estoque
✅ Área administrativa do Django

**🔐 Área Administrativa**
Acesse:
http://127.0.0.1:8000/admin/

Usuário: admin
Senha: admin

**📂 Estrutura do Projeto**
code/
│
├── cooperativa/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── plataforma/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── manage.py
└── db.sqlite3
🖼️ Arquivos Estáticos

**📖 Tecnologias Utilizadas**
Python
Django
SQLite
HTML5
CSS3
Bootstrap
JavaScript
Chart.js

**🔒 Controle de Acesso**
O sistema utiliza autenticação do Django:
Login
Logout
Registro de usuários
Controle por perfil:
Produtor
Cliente

📖 **Documentação**
Documentação oficial do Django:
Django Documentation

**🌱 Objetivo do Projeto**
O projeto foi desenvolvido para auxiliar cooperativas agrícolas no gerenciamento de suas atividades.

**📌 Observações**
Caso ocorram problemas com migrations:

python3 manage.py makemigrations
python3 manage.py migrate

Caso o banco apresente conflitos:
del db.sqlite3

Depois execute novamente:

python3 manage.py migrate

**🎓 Projeto Acadêmico****
Projeto desenvolvido para a disciplina de Programação Web.

🚜 **Cooperativa Agrícola**

Sistema acadêmico para gerenciamento agrícola utilizando Django.

