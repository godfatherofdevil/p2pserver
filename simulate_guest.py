import requests
import random

from stun_client import get_public_address
from server.log import logger


def get_available_sessions():
    url = "http://localhost:8000/games"

    with requests.Session() as http_session:
        response = http_session.get(url)

    if response.status_code != 200:
        return []
    else:
        return response.json()


def start_game_session():
    start_url = "http://localhost:8000/games/start"
    sessions = get_available_sessions()

    while True:
        session = random.choice(sessions)
        addresses = get_public_address()
        game, peer_id = session.get("name"), session.get("peerId")
        logger(f"trying to start game = {game}, peer = {peer_id}")
        req_data = {
            "name": game,
            "peerId": peer_id,
            "addresses": addresses
        }
        with requests.Session() as http_client:
            response = http_client.post(start_url, json=req_data)
        response_json = response.json()
        if response_json.get("status") == 1:
            logger(f"found a host address to connect to = {response_json.get('addresses')}")
            break
        else:
            logger(f"no host found to connect to. continuing")
            continue


if __name__ == "__main__":
    start_game_session()
