import logging
import requests



def download_crypto(moeda: str, qtd: str) -> str:
    """Baixa um conjunto de dados de cripyto moedas e retorna o conteúdo json."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    logging.info(f"Iniciando a extração das cripto {url}")

    
    response = requests.get(url, params={"vs_currency": moeda, "order": "market_cap_desc", "per_page": qtd, "page": "1"})
    response.raise_for_status()  # levanta erro se status != 200

    return response.json()