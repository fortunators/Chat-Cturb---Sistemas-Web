# Importação das bibliotecas necessárias
import json          # Manipulação de dados em formato JSON
import base64        # Decodificação e codificação Base64 (padrão usado pelo Firehose)
from datetime import datetime  # Obtenção da data/hora atual
from zoneinfo import ZoneInfo  # Controle de fuso horário (substitui pytz nas versões mais novas do Python)

# ---------------------------------------------------------------------
# Função auxiliar para imprimir logs formatados no console
# ---------------------------------------------------------------------
def formatar_e_imprimir_log(titulo, log_dict):
    """Imprime logs de forma organizada e hierárquica."""
    print(f"--- {titulo} ---")
    for key, value in log_dict.items():
        # Se o valor for um dicionário, imprime com indentação para melhor visualização
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            # Caso contrário, imprime normalmente
            print(f"{key}: {value}")
    # Linha divisória para clareza visual
    print("----------------------------------" + "-" * len(titulo))


# ---------------------------------------------------------------------
# Função principal: responsável por transformar e anonimizar os dados
# ---------------------------------------------------------------------
def transformar_dados_para_analytics(evento_do_firehose):
    """
    Microsserviço acionado pelo Firehose para transformar dados em lote
    antes do armazenamento final. Realiza a anonimização de dados sensíveis.
    """

    # Captura a data e hora atual com fuso horário de São Paulo
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # Contador para acompanhar quantos registros foram processados
    registros_processados = 0

    # Loop sobre todos os registros recebidos do evento Firehose
    for registro in evento_do_firehose.get('records', []):
        # 1️⃣ Decodifica o dado que vem em Base64 (padrão do Firehose)
        dados_originais_str = base64.b64decode(registro['data']).decode('utf-8')

        # 2️⃣ Converte a string JSON em um dicionário Python
        dados_originais = json.loads(dados_originais_str)

        # Cria uma cópia dos dados originais para não alterar a referência original
        dados_transformados = dados_originais.copy()

        # 3️⃣ Verifica se há um campo de usuário que precisa ser anonimizado
        if 'usuario_id' in dados_transformados.get('dados_do_evento', {}):
            id_original = dados_transformados['dados_do_evento']['usuario_id']

            # Gera um identificador anônimo (simples hash numérico truncado)
            id_anonimizado = f"user_{hash(id_original) % 10000}"

            # Substitui o ID original pelo anonimizado
            dados_transformados['dados_do_evento']['usuario_id'] = id_anonimizado

        # Incrementa o contador de registros processados
        registros_processados += 1

        # Monta um dicionário de log para registrar a transformação
        log_transformacao = {
            "data/hora": data_hora,
            "servico": "transformar_dados_analytics",
            "status": "TRANSFORMADO COM SUCESSO",
            "dado_original": dados_originais.get('dados_do_evento'),
            "dado_anonimizado": dados_transformados.get('dados_do_evento')
        }

        # Chama a função auxiliar para imprimir o log da transformação
        formatar_e_imprimir_log(f"Transformação do Registro #{registros_processados}", log_transformacao)

    # Exibe o total de registros processados no final
    print(f"\nTotal de {registros_processados} registros de analytics processados e anonimizados.")

    # Retorna True para indicar sucesso (padrão simples de retorno)
    return True


# ---------------------------------------------------------------------
# Bloco de simulação local — serve apenas para testes fora da AWS
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("Teste do microsserviço 'TransformarDadosAnalytics'\n")

    # Simulação do evento que o Firehose enviaria para a função Lambda
    evento_firehose_simulado = {
        "records": [
            {
                # ID do registro (geralmente fornecido pelo Firehose)
                "recordId": "4966...",
                # Dado codificado em Base64 simulando o que viria do Firehose
                "data": base64.b64encode(json.dumps({
                    "servico": "analytics",
                    "status": "EVENTO COLETADO",
                    "dados_do_evento": {
                        "tipo_evento": "MENSAGEM_ENVIADA",
                        "usuario_id": "Gustavo Fortunato"
                    }
                }).encode('utf-8'))
            },
            {
                "recordId": "4967...",
                "data": base64.b64encode(json.dumps({
                    "servico": "analytics",
                    "status": "EVENTO COLETADO",
                    "dados_do_evento": {
                        "tipo_evento": "LOGIN_APP",
                        "usuario_id": "Marlon"
                    }
                }).encode('utf-8'))
            }
        ]
    }

    # Mensagem indicativa de que o lote de eventos será processado
    print("[Processando lote de eventos do Firehose para transformação]")

    # Chama a função principal simulando o fluxo real do microsserviço
    transformar_dados_para_analytics(evento_firehose_simulado)
