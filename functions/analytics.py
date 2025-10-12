import uuid
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
    print("----------------------------" + "-" * len(titulo))

def coletar_evento_analytics(dados_do_evento):
    """
    Microsserviço que recebe um evento de analytics via API
    e o envia para o stream do Kinesis Firehose.
    """
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")
    tipo_evento = dados_do_evento.get('tipo_evento')

    if not tipo_evento:
        log_falha = {
            "data/hora": data_hora, "servico": "analytics",
            "status": "FALHA NA COLETA",
            "motivo": "O campo 'tipo_evento' é obrigatório.",
        }
        formatar_e_imprimir_log("Falha no Evento de Analytics", log_falha)
        return False

    log_coleta = {
        "data/hora": data_hora, "servico": "analytics",
        "status": "EVENTO COLETADO",
        "mensagem": f"Evento '{tipo_evento}' recebido e enviado para o Firehose.",
        "dados_do_evento": dados_do_evento
    }

    # Em um cenário real, o log_coleta seria enviado para o Firehose aqui.
    formatar_e_imprimir_log("Detalhes do Evento Coletado", log_coleta)
    return True

# --- Bloco de Simulação para Apresentação ---
if __name__ == "__main__":
    print("Teste do microsserviço 'Analytics'\n")

    evento_de_uso = {
        "evento_id": str(uuid.uuid4()),
        "tipo_evento": "MENSAGEM_ENVIADA",
        "usuario_id": "Gustavo Fortunato",
        "detalhes": {
            "tamanho_da_mensagem_bytes": 45,
            "contem_anexo": False
        }
    }

    print("[Processando evento de analytics da API]")
    coletar_evento_analytics(evento_de_uso)