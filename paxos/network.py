import concurrent.futures
import requests
import logging
from typing import Optional


def send(node: str, url: str, raw_message: dict) -> dict | None:
    try:
        response = requests.post(f"http://{node}{url}",
                                 json=raw_message,
                                 timeout=1000)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        logging.getLogger("requests").warning(exc)


def send_to_all(nodes: list[str], url: str, raw_message: dict) -> list[dict | None]:
    def send_one(node):
        return send(node, url, raw_message)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return list(executor.map(send_one, nodes))
