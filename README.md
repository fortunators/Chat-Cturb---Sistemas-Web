# 📡 Microserviços de Mensageria e Analytics (Python)

Este projeto simula um **pipeline de microsserviços em Python** que processa mensagens, realiza análises de uso, envia notificações e trata erros de forma isolada.  
Cada módulo representa uma função que poderia ser executada em **AWS Lambda**, integrando com serviços como **API Gateway**, **SNS**, **SQS** e **Kinesis Firehose**.

---

## 🧩 Estrutura do Projeto

```
📁 projeto/
├── analytics.py
├── transformar_dados_analytics.py
├── processarMensagem.py
├── enviarMensagem.py
├── Notificacao_de_erro.py
└── notificar_usuario.py
```

---

## 🚀 Visão Geral dos Microsserviços

### 1️⃣ `analytics.py`
- Coleta eventos de uso (ex: mensagens enviadas, logins, cliques).
- Simula o envio dos eventos para o **Kinesis Firehose**.
- Gera logs detalhados com horário e tipo de evento.

🧩 **Função principal:** `coletar_evento_analytics(dados_do_evento)`

---

### 2️⃣ `transformar_dados_analytics.py`
- Recebe dados do Firehose e transforma o lote antes do armazenamento.
- Realiza **anonimização de dados sensíveis** (LGPD).
- Mostra logs com o dado original e o dado anonimizado.

🧩 **Função principal:** `transformar_dados_para_analytics(evento_do_firehose)`

---

### 3️⃣ `processarMensagem.py`
- Processa mensagens recebidas via **API Gateway**.
- Valida campos obrigatórios (`remetente_id`, `destinatario_id`, `mensagem`).
- Retorna o payload preparado para envio.

🧩 **Função principal:** `processar_mensagem(event)`

---

### 4️⃣ `enviarMensagem.py`
- Simula o envio de mensagens para uma fila **SNS**.
- Exibe logs de sucesso ou erro durante o envio.
- Em uma aplicação real, utilizaria o `boto3` para integração com AWS.

🧩 **Função principal:** `enviar_mensagem(event)`

---

### 5️⃣ `Notificacao_de_erro.py`
- Acionado quando há falha crítica (ex: mensagens movidas para uma **Dead-Letter Queue - DLQ**).
- Registra detalhes do erro e simula o envio de um alerta à equipe técnica.

🧩 **Função principal:** `registrar_erro_processamento(dados_do_erro)`

---

### 6️⃣ `notificar_usuario.py`
- Simula o envio de uma **notificação ao usuário final** após o processamento da mensagem.
- Acionado pelo **SNS (Simple Notification Service)**.
- Exibe logs estruturados e seguros (sem expor a mensagem completa).
- Demonstra boas práticas de **observabilidade** e **princípio DRY (Don't Repeat Yourself)**.

🧩 **Função principal:** `enviar_notificacao_usuario(dados_da_notificacao)`

---

## 🧱 Tecnologias Utilizadas

- **Python 3.10+**
- **ZoneInfo** (para timezone local)
- **UUID** (para identificação única de eventos)
- **Base64 & JSON** (para simular codificação dos dados)
- **AWS conceitos simulados:** SNS, SQS, API Gateway, Kinesis Firehose

---

## 🧪 Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Execute qualquer microsserviço diretamente:
   ```bash
   python analytics.py
   python transformar_dados_analytics.py
   python processarMensagem.py
   python enviarMensagem.py
   python Notificacao_de_erro.py
   python notificar_usuario.py
   ```

3. Cada script exibe **logs detalhados** simulando o fluxo de dados entre os serviços.

---

## 🧵 Fluxo de Dados Simulado

```
[API Gateway] → processarMensagem.py
                    ↓
               enviarMensagem.py → [SNS/SQS]
                    ↓
             notificar_usuario.py
                    ↓
                analytics.py → transformar_dados_analytics.py
                    ↓
           [Firehose + Armazenamento final]
                    ↓
         Notificacao_de_erro.py (em caso de falhas)
```

---

## 📋 Exemplos de Uso

### Processar Mensagem
```python
from processarMensagem import processar_mensagem
evento = {
    "body": '{"remetente_id": "User1", "destinatario_id": "User2", "mensagem": "Olá!"}'
}
print(processar_mensagem(evento))
```

### Coletar Evento Analytics
```python
from analytics import coletar_evento_analytics
coletar_evento_analytics({"tipo_evento": "LOGIN_APP", "usuario_id": "User1"})
```

### Notificar Usuário
```python
from notificar_usuario import enviar_notificacao_usuario
enviar_notificacao_usuario({
    "remetente_id": "Sistema",
    "destinatario_id": "User2",
    "texto_mensagem": "Sua solicitação foi concluída!"
})
```

---

## 🧑‍💻 Autores

**Gustavo Fortunato**  
**Kayque**  
**Nycollas**  

💼 Projeto acadêmico/simulador de microsserviços em Python  
📍 Foco em boas práticas de logs, modularização e simulação de arquitetura em nuvem.

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT.  
Sinta-se livre para usar, modificar e contribuir!

---

## 🧠 Ideias Futuras

- Integração real com AWS (`boto3`)
- Logs estruturados em JSON
- Testes unitários (pytest)
- Pipeline CI/CD
