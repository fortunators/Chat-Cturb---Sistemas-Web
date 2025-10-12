# enviar_mensagem.py
import json
from datetime import datetime
from zoneinfo import ZoneInfo


def formatar_e_imprimir_log(titulo, log_dict):
    """
    Função auxiliar para formatação e exibição de logs estruturados no console.
    - Exibe um título destacado.
    - Percorre o dicionário de log e imprime suas chaves e valores.
    - Suporta dicionários aninhados para exibir logs mais detalhados.
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


def enviar_mensagem(event):
    """
    Microsserviço responsável por simular o envio de mensagens para o serviço SNS.
    
    Fluxo principal:
      1. Recebe um evento contendo uma mensagem processada.
      2. Valida se o campo 'mensagem_processada' está presente.
      3. Caso válido, registra um log de sucesso com informações detalhadas.
      4. Caso inválido, gera e imprime um log de erro.
    
    Observação:
      Em um ambiente real, o envio seria feito via AWS SNS usando a biblioteca boto3.
    """
    # Captura o horário atual no fuso de São Paulo
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")
    
    # Extrai a mensagem processada do evento recebido
    mensagem = event.get("mensagem_processada")

    # Validação: se não houver mensagem, registra erro e retorna
    if not mensagem:
        erro = {
            "erro": "Nenhuma mensagem processada foi recebida.",
            "evento": event
        }
        formatar_e_imprimir_log("ERRO AO ENVIAR MENSAGEM", erro)
        return {"status": "erro", "detalhes": erro}

    # Simulação do envio da mensagem (substituir por boto3 em produção)
    log_envio = {
        "data/hora": data_hora,
        "servico": "enviar_mensagem",
        "status": "Mensagem enviada com sucesso ao SNS.",
        "mensagem_enviada": mensagem
    }

    # Exibe o log de sucesso
    formatar_e_imprimir_log("MENSAGEM ENVIADA", log_envio)
    return {"status": "ok", "detalhes": log_envio}


# --- Execução local para teste do microsserviço ---
if __name__ == "__main__":
    print("Teste do microsserviço 'enviar_mensagem'\n")

    # Evento de exemplo simulando uma mensagem já processada
    evento_teste = {
        "mensagem_processada": {
            "remetente_id": "Kayque Santos",
            "destinatario_id": "Lucas Felipe",
            "mensagem": "Olá! Sua solicitação foi concluída com sucesso."
        }
    }

    print("[Enviando mensagem simulada ao SNS]")
    resultado = enviar_mensagem(evento_teste)
    print("\nResultado final:", resultado)
