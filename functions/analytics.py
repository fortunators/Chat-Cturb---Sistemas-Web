# ---------------------------------------------------------------------
# Importações de bibliotecas padrão
# ---------------------------------------------------------------------
import uuid                          # Gera identificadores únicos universais (UUIDs) para os eventos
from datetime import datetime        # Usado para capturar a data e hora atuais
from zoneinfo import ZoneInfo        # Permite definir fuso horário de forma moderna e precisa (substitui pytz)

# ---------------------------------------------------------------------
# Função auxiliar: imprime logs de forma organizada e hierárquica
# ---------------------------------------------------------------------
def formatar_e_imprimir_log(titulo, log_dict):
    """Função auxiliar para imprimir logs no formato desejado."""
    print(f"--- {titulo} ---")
    for key, value in log_dict.items():
        # Caso o valor seja outro dicionário, imprime com indentação
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            # Caso contrário, imprime diretamente a chave e o valor
            print(f"{key}: {value}")
    # Linha divisória para melhor legibilidade dos logs
    print("----------------------------" + "-" * len(titulo))

# ---------------------------------------------------------------------
# Função principal: coleta de evento analítico
# ---------------------------------------------------------------------
def coletar_evento_analytics(dados_do_evento):
    """
    Microsserviço que recebe um evento de analytics via API
    e o envia para o stream do Kinesis Firehose.
    
    Em uma arquitetura real, essa função seria chamada por uma API Gateway + Lambda,
    e o evento seria encaminhado para o Firehose (ou Kafka) para posterior processamento.
    """

    # Captura a data/hora atual no fuso horário de São Paulo
    data_hora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d-%m-%Y %H:%M:%S")

    # Lê o tipo do evento, campo obrigatório para identificar o tipo de ação do usuário
    tipo_evento = dados_do_evento.get('tipo_evento')

    # -----------------------------------------------------------------
    # Validação: o campo 'tipo_evento' é obrigatório
    # -----------------------------------------------------------------
    if not tipo_evento:
        # Caso o evento não contenha o campo necessário, gera log de falha
        log_falha = {
            "data/hora": data_hora,
            "servico": "analytics",
            "status": "FALHA NA COLETA",
            "motivo": "O campo 'tipo_evento' é obrigatório.",
        }
        # Imprime log detalhado do erro
        formatar_e_imprimir_log("Falha no Evento de Analytics", log_falha)
        return False  # Retorna False indicando falha no processamento

    # -----------------------------------------------------------------
    # Caso o evento seja válido, registra sucesso e prepara para envio
    # -----------------------------------------------------------------
    log_coleta = {
        "data/hora": data_hora,
        "servico": "analytics",
        "status": "EVENTO COLETADO",
        "mensagem": f"Evento '{tipo_evento}' recebido e enviado para o Firehose.",
        "dados_do_evento": dados_do_evento  # Inclui o payload completo do evento
    }

    # Em um ambiente real, aqui haveria o envio do evento ao Kinesis Firehose:
    # firehose_client.put_record(DeliveryStreamName="analytics_stream", Record={"Data": json.dumps(log_coleta)})
    # Mas para fins de demonstração, apenas imprimimos no console.
    formatar_e_imprimir_log("Detalhes do Evento Coletado", log_coleta)

    # Retorna True indicando sucesso na coleta e envio
    return True


# ---------------------------------------------------------------------
# Bloco de simulação: serve para testar o funcionamento localmente
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("Teste do microsserviço 'Analytics'\n")

    # Simula um evento real recebido por uma API, com identificador único
    evento_de_uso = {
        "evento_id": str(uuid.uuid4()),  # Gera um ID único (simulando ID gerado pelo sistema de coleta)
        "tipo_evento": "MENSAGEM_ENVIADA",  # Tipo de evento sendo registrado
        "usuario_id": "Gustavo Fortunato",  # Usuário responsável pelo evento
        "detalhes": {                      # Informações complementares do evento
            "tamanho_da_mensagem_bytes": 45,
            "contem_anexo": False
        }
    }

    # Log informativo para o início do processamento
    print("[Processando evento de analytics da API]")

    # Chamada da função principal simulando o fluxo de um evento real
    coletar_evento_analytics(evento_de_uso)
