# Planos de Teste - Sistema de Autenticação

## TP-1: Login - Credenciais Válidas

**Nome:** Login - Credenciais Válidas

**Objetivo/Escopo:**
- Verificar se o login ocorre com sucesso quando as credenciais estão corretas.
- Garantir que o usuário é redirecionado à página principal ou dashboard.

**Principais Passos:**
1. Ter um usuário válido cadastrado (ex: `usuarioValido`, `senhaValida`).
2. Acessar a tela de login.
3. Informar `usuarioValido` e `senhaValida`.
4. Clicar em Entrar.
5. Verificar redirecionamento para a tela principal/dados de usuário.

**Critérios de Aceite:**
- Usuário deve ser direcionado ao dashboard.
- Navbar ou similar deve exibir que o usuário está logado (ex.: "Logout").

**Tipo de Plano:** Smoke
**Produto:** Authenticator

---

## TP-2: Login - Senha Inválida

**Nome:** Login - Senha Inválida

**Objetivo/Escopo:**
- Validar o comportamento do sistema ao inserir senha incorreta.
- Verificar exibição de mensagem de erro e prevenção de acesso não autorizado.

**Principais Passos:**
1. Utilizar `usuarioValido` e `senhaIncorreta`.
2. Clicar em Entrar.
3. Conferir se o acesso é negado.
4. Verificar a mensagem de erro "Credenciais inválidas", com a classe alert-danger, componente:

```
Credenciais inválidas
```

**Critérios de Aceite:**
- Sem redirecionamento para áreas autenticadas.
- Mensagem de erro clara é exibida.

**Tipo de Plano:** Acceptance
**Produto:** Authenticator

---

## TP-3: Login - Campos em Branco

**Nome:** Login - Campos em Branco

**Objetivo/Escopo:**
- Garantir que o sistema não permita login com campos obrigatórios vazios.
- Verificar mensagens de validação adequadas. Nesse caso, a ausência de avisos, é bloqueado via serviço cliente Pelo próprio component input HTML.

**Principais Passos:**
1. Deixar os campos Usuário e Senha em branco e variações, 3 intervalos. (vazio, vazio) (preenchido, vazio), (vazio, preenchido)... a depender da quantidade de inputs
2. Clicar em Entrar.

**Critérios de Aceite:**
- Nenhum acesso concedido.
- Mensagem clara de "Campos obrigatórios" ou similar é exibida.

**Tipo de Plano:** Function
**Produto:** Authenticator

---

## TP-4: Login - Esqueci Minha Senha

**Nome:** Login - Esqueci Minha Senha

**Objetivo/Escopo:**
- Verificar o fluxo de recuperação de senha, que pode envolver serviços de e-mail.
- Confirmar redirecionamento correto para a página de redefinição.

**Principais Passos:**
1. Acessar a tela de login.
2. Clicar em Esqueci Minha Senha.
3. Inserir um e-mail válido (quando a funcionalidade estiver completa).
4. Verificar se um link de redefinição é enviado, mock smtp pode ser usado nesse caso.

**Critérios de Aceite:**
- Navegação para a página de redefinição sem forçar login.
- E-mail de recuperação (quando aplicável) é recebido.

**Tipo de Plano:** Smoke
**Produto:** Authenticator

---

## TP-5: Login - Link de Registro

**Nome:** Login - Link de Registro

**Objetivo/Escopo:**
- Conferir a disponibilidade do link de registro na tela de login.
- Validar a navegação para a página de cadastro, conferindo comportamento geral do sistema.

**Principais Passos:**
1. Na tela de login, localizar o Link de Registro (ex.: "Registrar").
2. Clicar nesse link.
3. Verificar se o sistema exibe o formulário de cadastro.
4. Devem ser testado as duas possibilidades, 'Registrar', na Barra de navegação e Não tem conta? Cadastre-se', no container de formulário de login.

**Critérios de Aceite:**
- O usuário é direcionado corretamente para a tela de registro.
- Não ocorre login automático ou erro.

**Tipo de Plano:** Integration
**Produto:** Authenticator

---

## TP-6: Register - Cadastro com Sucesso

**Nome:** Register - Cadastro com Sucesso

**Objetivo/Escopo:**
- Verificar se novos usuários podem se cadastrar com sucesso.
- Garantir que todos os campos são processados corretamente.

**Principais Passos:**
1. Acessar a página de registro.
2. Preencher username único no campo USERNAME_INPUT.
3. Preencher email único no campo EMAIL_INPUT.
4. Inserir senha no campo PASSWORD1_INPUT.
5. Confirmar senha no campo PASSWORD2_INPUT.
6. Clicar no botão SUBMIT_BUTTON.
7. Verificar redirecionamento e mensagem de confirmação.

**Critérios de Aceite:**
- Cadastro concluído com sucesso.
- Redirecionamento para tela de login ou dashboard.
- Mensagem de confirmação exibida.

**Tipo de Plano:** Integration
**Produto:** Authenticator

---

## TP-7: Register - Username já Existente

**Nome:** Register - Username já Existente

**Objetivo/Escopo:**
- Verificar se o sistema impede cadastro duplicado de usernames.
- Validar mensagens de erro apropriadas.

**Principais Passos:**
1. Acessar a página de registro.
2. Tentar cadastrar com username já existente.
3. Preencher demais campos com dados válidos.
4. Clicar no botão de cadastro.
5. Verificar mensagem de erro.

**Critérios de Aceite:**
- Cadastro não é permitido.
- Mensagem específica sobre username duplicado.
- Usuário permanece na tela de registro.

**Tipo de Plano:** Function
**Produto:** Authenticator

---

## TP-8: Register - Email já Existente

**Nome:** Register - Email já Existente

**Objetivo/Escopo:**
- Verificar se o sistema impede cadastro com email já existente.
- Validar mensagens de erro apropriadas.

**Principais Passos:**
1. Acessar a página de registro.
2. Preencher username único.
3. Inserir email já cadastrado.
4. Preencher senhas válidas.
5. Clicar no botão de cadastro.
6. Verificar mensagem de erro.

**Critérios de Aceite:**
- Cadastro não é permitido.
- Mensagem específica sobre email duplicado.
- Usuário permanece na tela de registro.

**Tipo de Plano:** Function
**Produto:** Authenticator

---

## TP-9: Register - Senhas Diferentes

**Nome:** Register - Senhas Diferentes

**Objetivo/Escopo:**
- Verificar validação quando as senhas não coincidem.
- Validar feedback ao usuário.

**Principais Passos:**
1. Acessar a página de registro.
2. Preencher username e email válidos.
3. Inserir senhas diferentes em PASSWORD1_INPUT e PASSWORD2_INPUT.
4. Submeter o formulário.
5. Verificar resposta do sistema.

**Critérios de Aceite:**
- Formulário não é submetido com sucesso.
- Mensagem clara sobre senhas não coincidentes.
- Usuário permanece na página de registro.

**Tipo de Plano:** Function
**Produto:** Authenticator

---

## TP-10: Register - Campos em Branco

**Nome:** Register - Campos em Branco

**Objetivo/Escopo:**
- Garantir que todos os campos obrigatórios sejam validados.
- Verificar feedback visual e textual para o usuário.

**Principais Passos:**
1. Acessar a página de registro.
2. Deixar um ou mais campos obrigatórios em branco.
3. Tentar submeter o formulário.
4. Verificar validações e mensagens.

**Critérios de Aceite:**
- Sistema impede cadastro incompleto.
- Indicação clara dos campos obrigatórios não preenchidos.
- Permanência na página de registro.

**Tipo de Plano:** Function
**Produto:** Authenticator

---

## TP-11: Forgot Password - Envio de Email

**Nome:** Forgot Password - Envio de Email

**Objetivo/Escopo:**
- Verificar se o sistema processa corretamente solicitações de recuperação de senha.
- Validar a experiência do usuário durante este fluxo.

**Principais Passos:**
1. Acessar a página de login.
2. Clicar no link de "Esqueci Minha Senha".
3. Inserir email cadastrado no sistema.
4. Submeter o formulário.
5. Verificar mensagem de confirmação.

**Critérios de Aceite:**
- Confirmação visual de que o email foi enviado.
- Sem exposição de informações sensíveis.
- Email de recuperação recebido (pode ser simulado em ambiente de teste).

**Tipo de Plano:** Integration
**Produto:** Authenticator

---

## TP-12: Forgot Password - Email Não Cadastrado

**Nome:** Forgot Password - Email Não Cadastrado

**Objetivo/Escopo:**
- Verificar comportamento do sistema quando email não existe.
- Garantir que não haja vazamento de informação.

**Principais Passos:**
1. Acessar página de recuperação de senha.
2. Inserir email não cadastrado.
3. Submeter formulário.
4. Verificar resposta do sistema.

**Critérios de Aceite:**
- Mensagem genérica que não indica se o email existe ou não.
- Proteção contra enumeração de usuários.
- Experiência consistente com email válido.

**Tipo de Plano:** Security
**Produto:** Authenticator

---

## TP-13: Dashboard - Acesso Autenticado

**Nome:** Dashboard - Acesso Autenticado

**Objetivo/Escopo:**
- Verificar se o dashboard é acessível apenas após autenticação.
- Validar exibição correta de informações do usuário logado.

**Principais Passos:**
1. Efetuar login com credenciais válidas.
2. Verificar redirecionamento para dashboard.
3. Validar elementos específicos do dashboard (HEADER_TITLE, STATS_SECTION, etc.).
4. Confirmar presença de opção de logout.

**Critérios de Aceite:**
- Dashboard carrega corretamente após login.
- Informações específicas do usuário são exibidas.
- Navegação interna funciona conforme esperado.

**Tipo de Plano:** Function
**Produto:** Authenticator

---

## TP-14: Dashboard - Tentativa de Acesso Não Autenticado

**Nome:** Dashboard - Tentativa de Acesso Não Autenticado

**Objetivo/Escopo:**
- Verificar proteção do dashboard contra acesso não autorizado.
- Validar redirecionamento para página de login.

**Principais Passos:**
1. Sem estar logado, tentar acessar URL do dashboard diretamente.
2. Verificar comportamento do sistema.

**Critérios de Aceite:**
- Redirecionamento para tela de login.
- Mensagem opcional explicando necessidade de autenticação.
- Após login bem-sucedido, retorno ao dashboard.

**Tipo de Plano:** Security
**Produto:** Authenticator

---

## TP-15: Home - Elementos para Usuário Não Autenticado

**Nome:** Home - Elementos para Usuário Não Autenticado

**Objetivo/Escopo:**
- Verificar se a página inicial exibe os elementos corretos para visitantes.
- Validar presença de links de login e registro.

**Principais Passos:**
1. Acessar a página inicial sem estar autenticado.
2. Verificar elementos visuais (HERO_TITLE, HERO_SUBTITLE).
3. Confirmar presença dos botões LOGIN_BUTTON e REGISTER_BUTTON.
4. Testar navegação para as páginas correspondentes.

**Critérios de Aceite:**
- Elementos visuais carregam corretamente.
- Links de login e registro funcionam.
- Informações gerais são apresentadas adequadamente.

**Tipo de Plano:** UI
**Produto:** Authenticator

---

## TP-16: Home - Elementos para Usuário Autenticado

**Nome:** Home - Elementos para Usuário Autenticado

**Objetivo/Escopo:**
- Verificar adaptação da página inicial para usuários logados.
- Validar presença de links para dashboard e logout.

**Principais Passos:**
1. Efetuar login.
2. Navegar para a página inicial.
3. Verificar elementos específicos para usuários autenticados.
4. Confirmar ausência de botões de login/registro.
5. Testar presença e funcionamento do DASHBOARD_BUTTON.

**Critérios de Aceite:**
- Interface adaptada para usuário logado.
- Acesso direto ao dashboard disponível.
- Opção de logout visível.

**Tipo de Plano:** UI
**Produto:** Authenticator