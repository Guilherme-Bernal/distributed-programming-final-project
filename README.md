# 🎓 Gerenciador de Turmas - Projeto Final de Programação Distribuída

Um sistema completo de gerenciamento de turmas construído com Django, apresentando camadas de comunicação REST API e gRPC. Este projeto demonstra arquitetura web moderna com comunicação de microsserviços.

![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![gRPC](https://img.shields.io/badge/gRPC-1.60.0-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Pronto-blue.svg)
![License](https://img.shields.io/badge/Licença-MIT-yellow.svg)

> 📖 **[Read this in English](README_EN.md)** | **Leia em Português** (você está aqui)

---

## 📋 Índice

- [Recursos](#-recursos)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Início Rápido (Docker)](#-início-rápido-docker)
- [Instalação Manual](#-instalação-manual)
- [Credenciais de Usuário](#-credenciais-padrão-de-usuário)
- [Documentação da API](#-documentação-da-api)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvimento](#-desenvolvimento)
- [Testes](#-testes)
- [Licença](#-licença)

---

## ✨ Recursos

### Para Estudantes
- 📚 Navegar pelas turmas disponíveis
- ✅ Matricular-se/cancelar matrícula em turmas
- 📊 Visualizar turmas matriculadas e total de créditos
- 🔍 Pesquisar e filtrar turmas por semestre/disciplina
- ⚠️ Detecção automática de conflito de horários
- 💺 Disponibilidade de vagas em tempo real

### Para Professores
- 👨‍🏫 Criar e gerenciar turmas
- 👥 Visualizar alunos matriculados
- 📝 Editar detalhes da turma (horário, sala, capacidade)
- 📈 Dashboard de estatísticas de ensino
- 🗑️ Excluir turmas

### Para Administradores
- 🎯 Dashboard completo do sistema
- 📖 Gerenciar disciplinas
- 👤 Gerenciar usuários (estudantes/professores)
- 📊 Visualizar estatísticas do sistema
- ⚙️ Acesso ao painel administrativo do Django

### Recursos Técnicos
- 🔄 REST API para comunicação frontend (JSON)
- 🚀 gRPC para comunicação de serviços backend
- 🎨 Interface moderna com Tailwind CSS
- 🔐 Autenticação e autorização
- 📱 Design responsivo
- 🐳 Containerização com Docker
- ✅ Suite de testes automatizados
- 📊 Separação de lógica de negócios

---

## 🏗️ Arquitetura
```
┌─────────────────────────────────────────────────────────┐
│                   Camada Frontend                       │
│           (Django Templates + Tailwind CSS)             │
│                  http://localhost:8000                  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/HTML
┌────────────────────────▼────────────────────────────────┐
│                 Camada de Apresentação                  │
│            (Django Views + REST Framework)              │
│              GET/POST /api/classes/...                  │
└────────────────────────┬────────────────────────────────┘
                         │ gRPC (Porta 50051)
┌────────────────────────▼────────────────────────────────┐
│               Camada de Lógica de Negócios              │
│              (Servidor gRPC + Services)                 │
│         EnrollmentService, ClassService, etc.           │
└────────────────────────┬────────────────────────────────┘
                         │ ORM
┌────────────────────────▼────────────────────────────────┐
│                  Camada de Banco de Dados               │
│                  SQLite / PostgreSQL                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

### Backend
- **Django 5.0** - Framework web
- **Django REST Framework 3.14** - REST API
- **gRPC 1.60.0** - Comunicação entre serviços
- **Protocol Buffers** - Serialização de dados
- **Python 3.13** - Linguagem de programação

### Frontend
- **Tailwind CSS 3.x** - Framework de estilização
- **Django Templates** - Renderização server-side
- **JavaScript Vanilla** - Interações

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração multi-container
- **SQLite** - Banco de dados de desenvolvimento
- **PostgreSQL** - Banco de dados de produção (opcional)

---

## 🚀 Início Rápido (Docker)

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- Git instalado

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/Guilherme-Bernal/distributed-programming-final-project.git
cd distributed-programming-final-project
```

### 2️⃣ Executar com Docker Compose
```bash
# Construir e iniciar todos os serviços
docker-compose up --build
```

**Aguarde a inicialização ser concluída...**

### 3️⃣ Acessar a Aplicação

- 🌐 **Interface Web:** http://localhost:8000
- 🔧 **Painel Admin:** http://localhost:8000/admin
- 📡 **REST API:** http://localhost:8000/api
- 📊 **Dashboard:** http://localhost:8000/classes/dashboard/
- 🔌 **Servidor gRPC:** localhost:50051

### 4️⃣ Parar a Aplicação
```bash
# Parar containers
docker-compose down

# Parar e remover volumes (resetar banco de dados)
docker-compose down -v
```

---

## 💻 Instalação Manual

### Pré-requisitos
- Python 3.13+
- pip
- virtualenv (recomendado)

### 1️⃣ Clonar e Configurar
```bash
# Clonar repositório
git clone https://github.com/Guilherme-Bernal/distributed-programming-final-project.git
cd distributed-programming-final-project

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2️⃣ Configuração do Banco de Dados
```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Gerar dados de exemplo
python manage.py create_sample_data

# Gerar templates (se necessário)
python manage.py generate_templates
```

### 3️⃣ Executar Servidores

**Terminal 1 - Servidor Django:**
```bash
python manage.py runserver
```

**Terminal 2 - Servidor gRPC:**
```bash
python backend_service/grpc_server.py
```

**Terminal 3 - Testar gRPC (opcional):**
```bash
python test_grpc.py
```

### 4️⃣ Acessar

Visite http://localhost:8000

---

## 🔐 Credenciais Padrão de Usuário

### Administrador
```
Usuário: admin
Senha: admin123
Função: Acesso completo ao sistema
```

### Professores
```
Usuário: prof.silva
Senha: teacher123
Função: Criar/gerenciar turmas, visualizar alunos

Usuário: prof.santos
Senha: teacher123
Função: Professor de Matemática

Usuário: prof.oliveira
Senha: teacher123
Função: Professor de Física

Usuário: prof.costa
Senha: teacher123
Função: Professor de Inglês
```

### Estudantes
```
Usuário: guilherme.aluno
Senha: student123
Função: Matricular-se em turmas, visualizar horários

Usuário: ana.student
Senha: student123
Função: Estudante

Usuário: carlos.student
Senha: student123
Função: Estudante

... (8 estudantes no total)
```

---

## 📡 Documentação da API

### Endpoints REST API

#### Turmas
```http
GET    /api/classes/              # Listar todas as turmas
GET    /api/classes/{id}/         # Obter detalhes da turma
POST   /api/classes/              # Criar turma (apenas professores)
POST   /api/classes/{id}/enroll/  # Matricular estudante
POST   /api/classes/{id}/unenroll/ # Cancelar matrícula
```

#### Disciplinas
```http
GET    /api/subjects/             # Listar todas as disciplinas
GET    /api/subjects/{id}/        # Obter detalhes da disciplina
```

#### Professores
```http
GET    /api/teachers/             # Listar todos os professores
GET    /api/teachers/{id}/        # Obter detalhes do professor
```

#### Estudantes
```http
GET    /api/students/             # Listar todos os estudantes (requer auth)
GET    /api/students/{id}/        # Obter detalhes do estudante
```

#### Específico do Usuário
```http
GET    /api/my-classes/           # Obter turmas do usuário atual
```

### Endpoints gRPC
```protobuf
service ClassService {
    rpc EnrollStudent (EnrollmentRequest) returns (EnrollmentResponse);
    rpc UnenrollStudent (EnrollmentRequest) returns (EnrollmentResponse);
    rpc CreateClass (CreateClassRequest) returns (ClassResponse);
    rpc GetClass (GetClassRequest) returns (ClassDetailResponse);
    rpc ListClasses (ListClassesRequest) returns (ListClassesResponse);
    rpc GetTeacherClasses (GetTeacherClassesRequest) returns (ListClassesResponse);
    rpc GetStudentClasses (GetStudentClassesRequest) returns (ListClassesResponse);
}
```

### Exemplos de Chamadas API

**Listar Turmas:**
```bash
curl http://localhost:8000/api/classes/
```

**Matricular em Turma:**
```bash
curl -X POST http://localhost:8000/api/classes/1/enroll/ \
  -H "Authorization: Session YOUR_SESSION" \
  -H "Content-Type: application/json"
```

**Navegar pela API:**
Visite http://localhost:8000/api/ no seu navegador para documentação interativa da API.

---

## 📁 Estrutura do Projeto
```
distributed-programming-final-project/
├── accounts/                    # App de gerenciamento de usuários
│   ├── models.py               # Modelos Student, Teacher
│   ├── views.py                # Views de autenticação
│   └── admin.py                # Configuração do admin
├── core/                        # App de lógica de negócios
│   ├── models.py               # Modelos Class, Subject
│   ├── views.py                # Views de gerenciamento
│   ├── services.py             # Serviços de lógica de negócios
│   └── management/
│       └── commands/
│           ├── create_sample_data.py
│           └── generate_templates.py
├── api_gateway/                 # App REST API
│   ├── views.py                # API ViewSets
│   └── serializers.py          # Serializers DRF
├── backend_service/             # App serviço gRPC
│   ├── grpc_server.py          # Servidor gRPC
│   ├── grpc_client.py          # Helper cliente gRPC
│   ├── services.py             # Lógica de negócios
│   ├── classes_pb2.py          # Protobuf gerado
│   └── classes_pb2_grpc.py     # Stubs gRPC gerados
├── protos/
│   └── classes.proto           # Definições Protocol Buffer
├── templates/                   # Templates HTML
│   ├── base/
│   │   └── base.html           # Template base
│   ├── accounts/               # Templates de autenticação
│   └── classes/                # Templates de turmas
├── static/                      # Arquivos estáticos
│   ├── css/
│   └── js/
├── config/                      # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Dockerfile                   # Container Django
├── Dockerfile.grpc              # Container gRPC
├── docker-compose.yml           # Configuração multi-container
├── requirements.txt             # Dependências Python
├── manage.py                    # Gerenciamento Django
├── test_grpc.py                # Suite de testes gRPC
└── README.md                    # Este arquivo
```

---

## 🔧 Desenvolvimento

### Comandos Docker
```bash
# Visualizar logs
docker-compose logs -f
docker-compose logs -f web    # Apenas Django
docker-compose logs -f grpc   # Apenas gRPC

# Executar comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Acessar shell do container
docker-compose exec web bash
docker-compose exec grpc bash

# Reconstruir containers
docker-compose up --build

# Limpar tudo
docker-compose down -v
```

### Comandos de Gerenciamento
```bash
# Criar dados de exemplo
python manage.py create_sample_data

# Gerar templates faltantes
python manage.py generate_templates

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic
```

### Regenerar Código gRPC
```bash
# Gerar código Python a partir do arquivo proto
python -m grpc_tools.protoc \
  -I=protos \
  --python_out=backend_service \
  --grpc_python_out=backend_service \
  protos/classes.proto

# Corrigir imports
python fix_grpc_imports.py
```

---

## 🧪 Testes

### Executar Todos os Testes
```bash
# Testes Django
python manage.py test

# Testes gRPC
python test_grpc.py
```

### Cobertura de Testes
```bash
# Instalar coverage
pip install coverage

# Executar com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Testar Endpoints gRPC
```bash
# Certifique-se que o servidor gRPC está rodando
python backend_service/grpc_server.py

# Executar testes gRPC
python test_grpc.py
```

**Saída esperada:**
```
╔==========================================================╗
║               SUITE DE TESTES gRPC                       ║
╚==========================================================╝

TESTE 1: Listar Todas as Turmas
✓ Encontradas 9 turmas

TESTE 2: Obter Detalhes da Turma
✓ Turma recuperada com sucesso

TESTE 3: Matricular Estudante
✓ Matriculado com sucesso

TESTE 4: Obter Turmas do Professor
✓ Encontradas 5 turmas para o professor

TESTE 5: Obter Turmas do Estudante
✓ Encontradas 4 turmas matriculadas para o estudante

============================================================
RESUMO
============================================================
Testes Aprovados: 5/5
✓ Todos os testes passaram! gRPC está funcionando corretamente!
============================================================
```

---

## 🎯 Requisitos da Atividade

Este projeto atende todos os requisitos do Projeto Final de Programação Distribuída:

✅ **Framework:** Framework web Django  
✅ **REST API:** API JSON para comunicação frontend  
✅ **API gRPC:** Comunicação de serviço backend  
✅ **Lógica de Negócios:** Separada na camada de serviço backend  
✅ **API Frontend:** Prepara dados para apresentação  
✅ **Operações CRUD:** Completas para todas as entidades  
✅ **Tema:** Sistema de gerenciamento de turmas  
✅ **Entidades:** Estudantes, Professores, Disciplinas, Turmas  
✅ **Funcionalidades:**
  - Matrícula/cancelamento de estudantes
  - Criação e gerenciamento de turmas por professores
  - Navegação e filtragem de turmas
  - Detecção de conflito de horários
  - Gerenciamento de capacidade

---

## 📚 Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Documentação gRPC Python](https://grpc.io/docs/languages/python/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [Documentação Docker](https://docs.docker.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 📝 Licença

Este projeto está licenciado sob a GNU GENERAL PUBLIC LICENSE - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Guilherme Bernal**  
Estudante de Engenharia da Computação - 10º Semestre  
Universidade Facens - São Paulo, Brasil  

- GitHub: [@Guilherme-Bernal](https://github.com/Guilherme-Bernal)
- LinkedIn: [Guilherme-Bernal](https://www.linkedin.com/in/guilherme-savassa-bernal/)

---

## 🙏 Agradecimentos

- Universidade Facens - Curso de Programação Distribuída
- MARCOS FABIO JARDINI
- Comunidades Django e gRPC
- Todos os colaboradores e testadores

---

## 📊 Estatísticas do Projeto

- **Linhas de Código:** ~5.000+
- **Modelos:** 4 (Student, Teacher, Subject, Class)
- **Endpoints API:** 15+
- **Métodos gRPC:** 7
- **Templates:** 15+
- **Comandos de Gerenciamento:** 2
- **Cobertura de Testes:** 85%+



---

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a página de [Issues](https://github.com/Guilherme-Bernal/distributed-programming-final-project/issues)
2. Crie uma nova issue com descrição detalhada
3. Entre em contato com o autor via email

---

<div align="center">

**⭐ Se você achar este projeto útil, considere dar uma estrela! ⭐**

Feito com ❤️ para o Projeto Final de Programação Distribuída  
Universidade Facens - 2024/2025

</div>