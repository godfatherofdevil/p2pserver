# this simulation will only work if the server is running and reachable
from uuid import uuid4
import random
import requests
import time

from server.log import logger
from stun_client import get_public_address

game_names = [
    "Minecraft", "Fortnite", "Counter-Strike", "League of Legends", "Age of Empires",
    "Assassin Creed", "Pubg", "Dead by Daylight", "Tetris 99", "Red dead online",
    "FIFA", "War Frame", "GTA online", "Overwatch", "Call of Duty"
]


def create_simulation_data(total=10):
    logger(f"registering {total} game sessions to start with.")
    url = "http://localhost:8000/games/register"
    registration_data, responses = [], []
    for t in range(total):
        peer_id = str(uuid4())
        game = random.choice(game_names)
        registration_data.append({"name": game, "peerId": peer_id})

    with requests.Session() as http_session:
        for data in registration_data:
            response = http_session.post(url, json=data)
            responses.append((response.status_code, response.json()))

    failed = list(filter(lambda resp: resp[0] != 200, responses))

    logger(f"success: {total - len(failed)}")

    return responses


if __name__ == "__main__":
    poll_url = "http://localhost:8000/games/poll"
    host_sessions = create_simulation_data()

    logger(f"polling p2p server for {len(host_sessions)} hosts")

    while True:
        # pick a random host session
        session = random.choice(host_sessions)
        addresses = get_public_address()
        game_data = session[1]
        game, peer_id = game_data.get("game"), game_data.get("peerId")
        logger(f"polling: host session , game= {game}, peerId = {peer_id}")
        req_data = {
            "name": game,
            "peerId": peer_id,
            "addresses": addresses
        }
        with requests.Session() as http_client:
            response = http_client.post(poll_url, json=req_data)
            response_json = response.json()
            if response_json.get("status") == 1:
                logger(f"found guest address to connect to: {response_json.get('addresses')}")
                break
            else:
                logger(f"no guest found to connect to - continuing")
                time.sleep(0.1)
                continue
