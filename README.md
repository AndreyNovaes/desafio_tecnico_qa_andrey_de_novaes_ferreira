# :closed_lock_with_key: Sistema de Testes Automatizados para Autenticação

<p align="justify">
Projeto de automação de testes para um sistema de autenticação completo, implementando o padrão Page Objects com Selenium WebDriver. Os testes validam funcionalidades como login, registro, recuperação de senha e dashboard, garantindo a qualidade e segurança do sistema de autenticação.
</p>

## :bookmark_tabs: Ferramentas e Tecnologias

- Python
- Selenium WebDriver
- PyTest
- Allure Reports
- Selenoid (Grid para execução paralela)
- Docker & Docker Compose
- Kiwi TCMS (Sistema de Gerenciamento de Casos de Teste)
- Serviço Faker para geração de dados de teste

## :rocket: Planos de Teste

O projeto implementa 16 planos de teste que cobrem todas as funcionalidades críticas do sistema de autenticação:

### Login
- **TP-1: Login - Credenciais Válidas** (Smoke) - Verifica login com sucesso e redirecionamento ao dashboard
- **TP-2: Login - Senha Inválida** (Acceptance) - Valida comportamento do sistema com credenciais inválidas
- **TP-3: Login - Campos em Branco** (Function) - Testa validação de campos obrigatórios
- **TP-4: Login - Esqueci Minha Senha** (Smoke) - Verifica fluxo de recuperação de senha
- **TP-5: Login - Link de Registro** (Integration) - Testa navegação para página de registro

### Registro
- **TP-6: Register - Cadastro com Sucesso** (Integration) - Verifica registro de novos usuários
- **TP-7: Register - Username já Existente** (Function) - Valida prevenção de duplicidade de username
- **TP-8: Register - Email já Existente** (Function) - Testa validação de emails já cadastrados
- **TP-9: Register - Senhas Diferentes** (Function) - Verifica validação de confirmação de senha
- **TP-10: Register - Campos em Branco** (Function) - Testa validação de campos obrigatórios no registro

### Recuperação de Senha
- **TP-11: Forgot Password - Envio de Email** (Integration) - Verifica envio de email de recuperação
- **TP-12: Forgot Password - Email Não Cadastrado** (Security) - Testa segurança contra enumeração de usuários

### Dashboard e Acessos
- **TP-13: Dashboard - Acesso Autenticado** (Function) - Verifica acesso ao dashboard por usuário logado
- **TP-14: Dashboard - Tentativa de Acesso Não Autenticado** (Security) - Testa proteção de rotas autenticadas
- **TP-15: Home - Elementos para Usuário Não Autenticado** (UI) - Verifica elementos da página inicial para visitantes
- **TP-16: Home - Elementos para Usuário Autenticado** (UI) - Valida adaptação da UI para usuários logados

## 💻 Como executar os testes

### Dependências mínimas
- Python 3.10+
- Docker: `Versão recomendada >= 20.10.x`
- Docker Compose: `Versão recomendada >= 2.3.x`

### Clone o projeto
```bash
git clone [URL do repositório]
cd [pasta do projeto]
```

### Configuração do ambiente virtual (opcional mas recomendado)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências, no caso do run_tests, é utilizado os containeres então não é necessário
pip install -r requirements.txt
```

### Execute os testes com o script automatizado
A maneira mais simples de executar todos os testes é usando o script `run_tests.py`, que:
- Verifica os pré-requisitos do sistema
- Inicia toda a infraestrutura necessária via Docker Compose
- Aguarda que todos os serviços estejam prontos
- Executa o conjunto completo de testes
- Exibe links para relatórios e ferramentas de monitoramento, como por exemplo o report do allure

```bash
python run_tests.py
```

Após a execução, você pode acessar os relatórios e serviços nos seguintes endereços:

```
# Relatórios Allure
http://localhost:5252

# Selenoid UI (visualizar sessões de teste em tempo real)
http://localhost:4444/ui

# Kiwi TCMS (Gerenciamento de casos de teste)
http://localhost:8080

# Logs dos containers (Dozzle)
http://localhost:8888
```

## :wrench: Infraestrutura

O projeto utiliza uma infraestrutura robusta baseada em containers Docker, conforme definido no arquivo `infra/docker-compose.yaml`:

- **web**: Aplicação Django de autenticação para testes (`autenticator/`)
- **selenoid**: Grid Selenium para execução de testes em diversos navegadores com gravação de vídeo
- **test**: Container que executa os testes automatizados em Selenium
- **kiwi** e **db**: Sistema de gerenciamento de casos de teste Kiwi TCMS e seu banco de dados MariaDB
- **allure** e **allure-ui**: Serviços para geração e visualização de relatórios detalhados
- **faker**: API para geração de dados aleatórios de teste, incluindo geradores para usuários, XSS, SQL, etc.
- **dozzle**: Interface para visualização de logs dos containers em tempo real
- **chrome-puller** e **video-recorder-puller**: Serviços para garantir que as imagens do Selenoid estejam disponíveis

A arquitetura permite a execução paralela de testes em múltiplos navegadores, gravação de vídeos das sessões, geração de relatórios detalhados e gerenciamento completo dos casos de teste.

![Infrastructure Diagram](docs/images/infrastructure.png)

## :test_tube: Estrutura do Projeto

```
📦teste-tecnico
 ┣ 📂autenticator/           # Aplicação Django para testes (sistema alvo)
 ┃ ┣ 📂accounts/             # App de autenticação do Django
 ┃ ┃ ┣ 📂templates/          # Templates HTML das páginas
 ┃ ┃ ┃ ┗ 📂accounts/
 ┃ ┃ ┃ ┃ ┣ 📜login.html      # Página de login
 ┃ ┃ ┃ ┃ ┣ 📜register.html   # Página de registro
 ┃ ┃ ┃ ┃ ┣ 📜dashboard.html  # Dashboard do usuário
 ┃ ┃ ┃ ┃ ┗ 📜...
 ┃ ┗ 📜...
 ┣ 📂infra/                  # Configuração da infraestrutura
 ┃ ┣ 📂config/               # Configurações do Selenoid
 ┃ ┣ 📂faker/                # API Faker para geração de dados de teste
 ┃ ┣ 📜docker-compose.yaml   # Definição de todos os serviços
 ┃ ┗ 📜...
 ┣ 📂page_objects_model_selenium/  # Framework de testes
 ┃ ┣ 📂locators/             # Localizadores de elementos da UI
 ┃ ┃ ┣ 📜base_locators.py    # Localizadores base
 ┃ ┃ ┣ 📜login_locators.py   # Localizadores da página de login
 ┃ ┃ ┣ 📜register_locators.py # Localizadores da página de registro
 ┃ ┃ ┗ 📜...
 ┃ ┣ 📂pages/                # Page Objects para interação com UI
 ┃ ┃ ┣ 📜base_page.py        # Classe base com métodos comuns
 ┃ ┃ ┣ 📜login_page.py       # Página de login
 ┃ ┃ ┣ 📜register_page.py    # Página de registro
 ┃ ┃ ┗ 📜...
 ┃ ┣ 📂tests/                # Testes automatizados
 ┃ ┃ ┣ 📜login_credenciais_validas_test.py
 ┃ ┃ ┣ 📜login_credenciais_invalidas_test.py
 ┃ ┃ ┣ 📜register_cadastro_sucesso_test.py
 ┃ ┃ ┗ 📜...
 ┃ ┣ 📂utils/                # Utilitários e helpers
 ┃ ┃ ┣ 📜webdriver_factory.py # Fábrica de WebDrivers
 ┃ ┃ ┣ 📜test_data.py        # Gerenciamento de dados de teste
 ┃ ┃ ┣ 📜faker_api_client.py # Cliente para API Faker
 ┃ ┃ ┗ 📜...
 ┃ ┣ 📜conftest.py           # Configurações do PyTest
 ┃ ┗ 📜pytest.ini            # Configurações adicionais do PyTest
 ┣ 📜run_tests.py            # Script principal para executar os testes
 ┣ 📜Planos_de_teste.md      # Documentação dos planos de teste
 ┗ 📜README.md
```

## 📊 Relatórios

### Allure Reports

Os relatórios Allure fornecem visualizações detalhadas dos resultados dos testes, incluindo:

- Estatísticas de execução
- Gráficos e tendências
- Screenshots de falhas
- Vídeos das sessões de teste
- Logs detalhados

### Kiwi TCMS

O Kiwi TCMS é usado para:

- Documentação de casos de teste
- Gestão de execuções de teste
- Rastreamento de bugs e issues
- Geração de relatórios gerenciais

## 🔍 Padrões e Boas Práticas

- **Page Object Model**: Separação clara entre lógica de teste e interação com UI
- **Fixture Reuse**: Reutilização de configurações através de fixtures do PyTest
- **Data Driven Testing**: Testes parametrizados com diferentes conjuntos de dados
- **Screenshot Capture**: Captura automática de screenshots em falhas
- **Video Recording**: Gravação de vídeo para análise detalhada de falhas
- **Cross-Browser Testing**: Execução em múltiplos navegadores via Selenoid
