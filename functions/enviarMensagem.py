# enviar_mensagem.py
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


def enviar_mensagem(event):
    """
    Microsserviço responsável por enviar mensagens para a fila SNS.
    Aqui é simulada a publicação no serviço.
    """
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")
    mensagem = event.get("mensagem_processada")

    if not mensagem:
        erro = {
            "erro": "Nenhuma mensagem processada foi recebida.",
            "evento": event
        }
        formatar_e_imprimir_log("ERRO AO ENVIAR MENSAGEM", erro)
        return {"status": "erro", "detalhes": erro}

    # Simulação do envio (em um cenário real, usaria boto3 para SNS)
    log_envio = {
        "data/hora": data_hora,
        "servico": "enviar_mensagem",
        "status": "Mensagem enviada com sucesso ao SNS.",
        "mensagem_enviada": mensagem
    }

    formatar_e_imprimir_log("MENSAGEM ENVIADA", log_envio)
    return {"status": "ok", "detalhes": log_envio}


# --- Simulação ---
if __name__ == "__main__":
    print("Teste do microsserviço 'enviar_mensagem'\n")

    evento_teste = {
        "mensagem_processada": {
            "remetente_id": "Gustavo Fortunato",
            "destinatario_id": "Lucas Felipe",
            "mensagem": "Olá! Sua solicitação foi concluída com sucesso."
        }
    }

    print("[Enviando mensagem simulada ao SNS]")
    resultado = enviar_mensagem(evento_teste)
    print("\nResultado final:", resultado)
