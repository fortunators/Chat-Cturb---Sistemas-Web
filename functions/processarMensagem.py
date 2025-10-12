# processar_mensagem.py
import json
from datetime import datetime
from zoneinfo import ZoneInfo


def formatar_e_imprimir_log(titulo, log_dict):
    """
    Função auxiliar para formatação e exibição de logs estruturados no console.
    - Exibe um título destacado.
    - Percorre o dicionário de log e imprime suas chaves e valores.
    - Suporta dicionários aninhados para detalhar informações.
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


def processar_mensagem(event):
    """
    Microsserviço responsável por processar a mensagem recebida via API Gateway.

    Funções principais:
      1. Ler e interpretar o corpo do evento (em formato JSON).
      2. Validar se todos os campos obrigatórios estão presentes.
      3. Preparar o payload final que será enviado à próxima etapa (ex: SQS ou SNS).
    
    Retornos possíveis:
      - status = "ok"  → mensagem válida e pronta para envio.
      - status = "erro" → falha de parsing ou ausência de campos obrigatórios.
    """
    # Captura o horário atual no fuso horário de São Paulo
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # Obtém o corpo do evento recebido do API Gateway
    corpo = event.get("body")

    # Tenta converter o corpo da requisição em JSON
    try:
        mensagem = json.loads(corpo)
    except (TypeError, json.JSONDecodeError):
        erro = {
            "erro": "Formato inválido de corpo. Esperado JSON válido.",
            "conteudo_recebido": corpo
        }
        formatar_e_imprimir_log("ERRO DE PARSING DE MENSAGEM", erro)
        return {"status": "erro", "detalhes": erro}

    # Define os campos obrigatórios da mensagem
    campos_obrigatorios = ["remetente_id", "destinatario_id", "mensagem"]

    # Verifica se algum campo obrigatório está ausente ou vazio
    faltando = [campo for campo in campos_obrigatorios if campo not in mensagem or not mensagem[campo]]

    if faltando:
        erro = {
            "erro": "Campos obrigatórios ausentes.",
            "campos_faltando": faltando,
            "mensagem_recebida": mensagem
        }
        formatar_e_imprimir_log("ERRO DE VALIDAÇÃO DE MENSAGEM", erro)
        return {"status": "erro", "detalhes": erro}

    # Cria log com informações da mensagem processada com sucesso
    log_processado = {
        "data/hora": data_hora,
        "servico": "processar_mensagem",
        "status": "Mensagem processada com sucesso.",
        "payload_preparado": mensagem
    }

    # Exibe o log formatado no console
    formatar_e_imprimir_log("MENSAGEM PROCESSADA", log_processado)

    # Retorna a mensagem validada e pronta para a próxima etapa
    return {"status": "ok", "mensagem_processada": mensagem}


# --- Execução local para teste do microsserviço ---
if __name__ == "__main__":
    print("Teste do microsserviço 'processar_mensagem'\n")

    # Evento de exemplo simulando a chamada do API Gateway
    evento_teste = {
        "body": json.dumps({
            "remetente_id": "Gustavo Fortunato",
            "destinatario_id": "Lucas Felipe",
            "mensagem": "Reunião confirmada para quarta-feira às 10h."
        })
    }

    print("[Iniciando processamento da mensagem]")
    resultado = processar_mensagem(evento_teste)
    print("\nResultado final:", resultado)
