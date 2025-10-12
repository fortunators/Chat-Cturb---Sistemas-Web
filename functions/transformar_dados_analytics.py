import json
import base64
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
    print("----------------------------------" + "-" * len(titulo))


def transformar_dados_para_analytics(evento_do_firehose):
    """
    Microsserviço acionado pelo Firehose para transformar dados em lote
    antes do armazenamento final. Realiza a anonimização de dados sensíveis.
    """
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")
    registros_processados = 0

    for registro in evento_do_firehose.get('records', []):
        # 1. Decodificar os dados recebidos (eles vêm em Base64 do Firehose)
        dados_originais_str = base64.b64decode(registro['data']).decode('utf-8')
        dados_originais = json.loads(dados_originais_str)

        # 2. A "Limpeza": Anonimizar o dado do usuário para proteger a privacidade (LGPD)
        dados_transformados = dados_originais.copy()
        if 'usuario_id' in dados_transformados.get('dados_do_evento', {}):
            id_original = dados_transformados['dados_do_evento']['usuario_id']
            # Técnica simples de hashing para gerar um ID anônimo
            id_anonimizado = f"user_{hash(id_original) % 10000}"
            dados_transformados['dados_do_evento']['usuario_id'] = id_anonimizado

        registros_processados += 1

        log_transformacao = {
            "data/hora": data_hora, "servico": "transformar_dados_analytics",
            "status": "TRANSFORMADO COM SUCESSO",
            "dado_original": dados_originais.get('dados_do_evento'),
            "dado_anonimizado": dados_transformados.get('dados_do_evento')
        }
        formatar_e_imprimir_log(f"Transformação do Registro #{registros_processados}", log_transformacao)

    print(f"\nTotal de {registros_processados} registros de analytics processados e anonimizados.")
    return True

# --- Bloco de Simulação para Apresentação ---
if __name__ == "__main__":
    print("Teste do microsserviço 'TransformarDadosAnalytics'\n")

    # Simula o lote de dados que o Kinesis Firehose enviaria para a Lambda
    evento_firehose_simulado = {
        "records": [
            {
                "recordId": "4966...",
                "data": base64.b64encode(json.dumps({
                    "servico": "analytics", "status": "EVENTO COLETADO",
                    "dados_do_evento": { "tipo_evento": "MENSAGEM_ENVIADA", "usuario_id": "Gustavo Fortunato" }
                }).encode('utf-8'))
            },
            {
                "recordId": "4967...",
                "data": base64.b64encode(json.dumps({
                    "servico": "analytics", "status": "EVENTO COLETADO",
                    "dados_do_evento": { "tipo_evento": "LOGIN_APP", "usuario_id": "Marlon" }
                }).encode('utf-8'))
            }
        ]
    }

    print("[Processando lote de eventos do Firehose para transformação]")
    transformar_dados_para_analytics(evento_firehose_simulado)