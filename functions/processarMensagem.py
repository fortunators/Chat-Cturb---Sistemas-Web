# processar_mensagem.py
import json
from datetime import datetime
from zoneinfo import ZoneInfo

def formatar_e_imprimir_log(titulo, log_dict):
    """Função auxiliar para imprimir logs no formato desejado."""
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
    Microsserviço responsável por processar a mensagem recebida
    via API Gateway, validar campos obrigatórios e preparar
    o payload para envio.
    """
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")
    corpo = event.get("body")

    try:
        mensagem = json.loads(corpo)
    except (TypeError, json.JSONDecodeError):
        erro = {
            "erro": "Formato inválido de corpo. Esperado JSON válido.",
            "conteudo_recebido": corpo
        }
        formatar_e_imprimir_log("ERRO DE PARSING DE MENSAGEM", erro)
        return {"status": "erro", "detalhes": erro}

    campos_obrigatorios = ["remetente_id", "destinatario_id", "mensagem"]
    faltando = [campo for campo in campos_obrigatorios if campo not in mensagem or not mensagem[campo]]

    if faltando:
        erro = {
            "erro": "Campos obrigatórios ausentes.",
            "campos_faltando": faltando,
            "mensagem_recebida": mensagem
        }
        formatar_e_imprimir_log("ERRO DE VALIDAÇÃO DE MENSAGEM", erro)
        return {"status": "erro", "detalhes": erro}

    log_processado = {
        "data/hora": data_hora,
        "servico": "processar_mensagem",
        "status": "Mensagem processada com sucesso.",
        "payload_preparado": mensagem
    }

    formatar_e_imprimir_log("MENSAGEM PROCESSADA", log_processado)
    return {"status": "ok", "mensagem_processada": mensagem}


# --- Simulação ---
if __name__ == "__main__":
    print("Teste do microsserviço 'processar_mensagem'\n")

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
