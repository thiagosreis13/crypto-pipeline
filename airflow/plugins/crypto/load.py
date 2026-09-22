import logging
from pymongo import MongoClient

def load_crypto(dados: list, crypto: str, host: str) -> None:
    """Conecta no banco de dados MongoDB e insere os dados na tabela"""
    client = MongoClient(f'mongodb://mongo:mongo@{host}:27017/')
    try:
        db = client["crypto_db"]        
        collection = db[crypto]

        collection.insert_many(dados)
    finally:
        client.close()