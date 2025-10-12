# Microsserviço: notificar_usuario
# Objetivo: Simular o envio de uma notificação para o usuário final.
# Contexto: Acionado pelo serviço SNS (Simple Notification Service) da AWS.

# Importamos as bibliotecas necessárias para trabalhar com datas e fusos horários.
# A biblioteca 'zoneinfo' é a forma moderna e recomendada de lidar com timezones em Python.
from datetime import datetime
from zoneinfo import ZoneInfo

def formatar_e_imprimir_log(titulo, log_dict):
    """
    Função auxiliar criada para padronizar a exibição dos logs.
    Isso evita a repetição de código (princípio DRY - Don't Repeat Yourself)
    e cria uma saída de texto limpa para a apresentação.
    """
    print(f"--- {titulo} ---")
    for key, value in log_dict.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    print("-------------------------" + "-" * len(titulo))


def enviar_notificacao_usuario(dados_da_notificacao):
    """
    Microsserviço principal, acionado pelo serviço SNS (Simple Notification Service).
    Sua única responsabilidade é pegar a mensagem e simular a entrega final
    para o dispositivo ou e-mail do usuário.
    """
    # 1. CAPTURA DE METADADOS: Capturamos o momento exato da execução.
    # Isso é fundamental para auditoria e monitoramento (observabilidade).
    # Usamos o fuso horário de São Paulo para garantir consistência.
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # 2. EXTRAÇÃO DE DADOS: Retiramos as informações essenciais do evento recebido do SNS.
    # O método .get() é uma forma segura de acessar chaves de um dicionário,
    # evitando erros caso a chave não exista (ele retorna um valor padrão, como 'N/A').
    destinatario_id = dados_da_notificacao.get('destinatario_id', 'N/A')
    texto = dados_da_notificacao.get('texto_mensagem', '...')

    # 3. CRIAÇÃO DO LOG ESTRUTURADO: Montamos um dicionário para registrar tudo o que aconteceu.
    # Logs estruturados (como este) são o padrão em sistemas na nuvem, pois
    # facilitam a busca e a criação de dashboards em ferramentas de monitoramento.
    log_envio = {
        "data/hora": data_hora,
        "servico": "notificar_usuario", # Identifica qual microsserviço gerou o log.
        "mensagem": f"Nova mensagem enviada com sucesso para o usuario '{destinatario_id}'.",
        "detalhes": {
            "usuario_notificado": destinatario_id,
            # Mostramos apenas um trecho da mensagem para não poluir o log e por privacidade.
            "preview_da_mensagem": f"{texto[:30]}..."
        }
    }

    # 4. AÇÃO FINAL: Usamos nossa função auxiliar para imprimir o log no terminal.
    # Em um sistema real, esta seria a etapa onde chamaríamos um outro serviço,
    # como o Amazon Pinpoint para enviar uma notificação push, ou o SES para enviar um e-mail.
    formatar_e_imprimir_log("Detalhes da Notificação", log_envio)

    return True

# --- BLOCO DE SIMULAÇÃO PARA APRESENTAÇÃO ---
# Este bloco de código só é executado quando rodamos o arquivo diretamente (`python notificar_usuario.py`).
# Ele NÃO é executado quando a função é chamada pela AWS Lambda. Serve para testar e demonstrar.
if __name__ == "__main__":
    print("Teste do microsserviço 'notificar_usuario'\n")

    # Criamos um dicionário de exemplo para simular os dados que o SNS enviaria.
    notificacao_do_sns = {
        "remetente_id": "Gustavo Fortunato",
        "destinatario_id": "Marlon",
        "tipo_mensagem": "texto",
        "texto_mensagem": "vai ter aula segunda?"
    }

    print("[Processando notificação do SNS para o usuário]")
    # Chamamos nossa função principal com os dados simulados.
    enviar_notificacao_usuario(notificacao_do_sns)