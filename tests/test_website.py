from main import app

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_startGame(client):
    response = client.get("/startgame")
    print(response.data)
    assert b"Winner is:" in response.data

def test_playerStats(client):
    response = client.get("/playerstats")
    print(response.data)
    assert b"Player 1" in response.data