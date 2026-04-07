from integrations.allegro.client import AllegroClient
from integrations.allegro.exceptions import AllegroAPIError

def get_offers(account):
    client = AllegroClient(account)

    response = client.get("/sale/offers")
    # response = client.get("/sale/product-offers/7781401037")

    if response.status_code != 200:
        raise AllegroAPIError(f"Error getting offers: {response.text}", status_code=response.status_code)

    return response.json()


def update_handling_time(account, offer_id, handling_time="PT24H"):
    client = AllegroClient(account)

    data = {
        "delivery": {
            "handlingTime": handling_time
        }
    }
    response = client.patch(f"/sale/product-offers/{offer_id}",data)
    if response.status_code not in (200, 202):
        raise AllegroAPIError(f"Error updating offer: {response.text}", status_code=response.status_code)
    return response.json()


