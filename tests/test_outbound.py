import requests

def test_outbound(base_url):
    r = requests.get(f"{base_url}/simulateOutbound")
    print(r.json())
