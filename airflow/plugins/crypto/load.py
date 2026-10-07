import logging
from pymongo import MongoClient, UpdateOne
from datetime import datetime, timezone

def load_crypto(dados: list, crypto: str, host: str) -> None:
    """
    Conecta no banco de dados MongoDB e insere os dados na collection
    gravação é idempotente: insere as moedas novas e ignora as que já existem por id + last_updated
    """
  
    client = MongoClient(f'mongodb://mongo:mongo@{host}:27017/')
    
    try:
        # Seleciona o banco e a collection de destino
        db = client["crypto_db"]        
        collection = db[crypto]

        # API sem retorno: avisa e sai sem gravar
        if len(dados) == 0:
            logging.warning("Coleção de dados veio vazia")

            return

        # Hora da coleta (UTC), única para o lote todo
        hr_atual = datetime.now(timezone.utc)

        # Banco impede duplicata de id + last_updated
        collection.create_index([("id", 1), ("last_updated", 1)], unique=True)

        # Uma operação por moeda: insere se não existir, ignora se existir
        operacoes_crypto = []
        for dado in dados:
            dado['extracted_at'] = hr_atual

            # Filtro com a chave de negócio: define se a moeda já existe no banco
            filtro = {"id": dado["id"], "last_updated": dado["last_updated"]}
            operacoes_crypto.append(UpdateOne(filtro, {"$setOnInsert": dado}, upsert=True))

        resultado_operacoes = collection.bulk_write(operacoes_crypto)
        logging.info(f"Moedas recebidas: {len(dados)}, novas: {resultado_operacoes.upserted_count}, existiam: {resultado_operacoes.matched_count}")
    finally:
        client.close()