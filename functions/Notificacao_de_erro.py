# Microsserviço: notificar_erro
# Objetivo: Registrar e alertar sobre erros críticos no processamento de mensagens.
# Contexto: Acionado quando uma mensagem falha repetidamente e é movida para uma
# Dead-Letter Queue (DLQ) no SQS.

# As importações e a função auxiliar são as mesmas do outro arquivo,
# mantendo a consistência do projeto.
from datetime import datetime
from zoneinfo import ZoneInfo

def formatar_e_imprimir_log(titulo, log_dict):
    """
    Função auxiliar criada para padronizar a exibição dos logs.
    """
    print(f"--- {titulo} ---")
    for key, value in log_dict.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
    print("------------------------" + "-" * len(titulo))


def registrar_erro_processamento(dados_do_erro):
    """
    Microsserviço de segurança, acionado quando uma mensagem falha repetidamente
    e é movida para uma Dead-Letter Queue (DLQ) no SQS.
    O objetivo é registrar a falha e alertar a equipe de desenvolvimento.
    """
    # 1. CAPTURA DE METADADOS: Novamente, registramos o tempo para auditoria.
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # 2. EXTRAÇÃO DE DADOS DO ERRO: Pegamos a mensagem original que causou a falha
    # e o contexto do erro (a explicação do porquê falhou).
    # Ter esses dados é essencial para que os desenvolvedores possam depurar o problema.
    mensagem_original = dados_do_erro.get('mensagem_que_falhou', {})
    contexto_erro = dados_do_erro.get('contexto_erro', 'Causa desconhecida')

    # 3. CRIAÇÃO DO LOG DE ALERTA: Montamos um log estruturado, mas desta vez
    # com um tom de urgência, pois representa uma falha no sistema.
    log_alerta = {
        "data/hora": data_hora,
        "servico": "notificar_erro", # Identifica a origem do alerta.
        "alerta": "FALHA CRÍTICA AO PROCESSAR MENSAGEM. Ação manual necessária.",
        "detalhes_erro": {
            "motivo_da_falha": contexto_erro,
            "mensagem_original": mensagem_original # Incluímos a "mensagem venenosa" inteira.
        }
    }

    # 4. AÇÃO FINAL: Simulamos o envio de um alerta para a equipe.
    # Em um sistema real, esta etapa poderia:
    # - Enviar uma mensagem para um canal do Slack.
    # - Abrir um chamado em uma ferramenta como PagerDuty ou Jira.
    # - Enviar um e-mail para a lista de distribuição da equipe de desenvolvimento.
    formatar_e_imprimir_log("ALERTA DE ERRO DE PROCESSAMENTO", log_alerta)

    return True

# --- BLOCO DE SIMULAÇÃO PARA APRESENTAÇÃO ---
if __name__ == "__main__":
    print("Teste do microsserviço 'notificar_erro'\n")

    # Criamos um exemplo de uma "mensagem venenosa" (poison pill).
    # É uma mensagem que o sistema não consegue processar por causa de um erro nos dados.
    mensagem_com_erro = {
        "contexto_erro": "O campo 'destinatario_id' é obrigatório e veio nulo.",
        "mensagem_que_falhou": {
            "remetente_id": "Gustavo Fortunato",
            "destinatario_id": None, # <<-- ESTE É O ERRO! O campo que causou a falha.
            "tipo_mensagem": "texto",
            "texto_mensagem": "Esta mensagem não será entregue."
        }
    }

    print("[Processando notificação de erro da DLQ]")
    # Chamamos a função com a mensagem de erro para demonstrar a captura da falha.
    registrar_erro_processamento(mensagem_com_erro)