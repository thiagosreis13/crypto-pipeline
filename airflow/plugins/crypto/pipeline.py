from crypto.extract import download_crypto
from crypto.load import load_crypto


def extract_load_dados(moeda: str, qtd: str, destino: str, host: str) -> None:

    data = download_crypto(moeda, qtd)
    load_crypto(data, destino, host)