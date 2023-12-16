import requests

from configs.settings import Settings
from models.ghostfolio_activity import GhostfolioActivity

activities = [
    GhostfolioActivity(
        account_id="fb6b8033-96b8-4d36-a879-a9b6c258265b",
        comment=None,
        currency="USD",
        date="2023-10-04T23:00:00.000Z",
        fee=0.33,
        quantity=12.13273,
        symbol="VGSH",
        type="DIVIDEND",
        unit_price=0.1788,
    ),
    GhostfolioActivity(
        account_id="fb6b8033-96b8-4d36-a879-a9b6c258265b",
        comment=None,
        currency="USD",
        date="2023-10-04T23:00:00.000Z",
        fee=0.0,
        quantity=0.032,
        symbol="VGSH",
        type="BUY",
        unit_price=57.5081,
    ),
    GhostfolioActivity(
        account_id="fb6b8033-96b8-4d36-a879-a9b6c258265b",
        comment=None,
        currency="USD",
        date="2023-10-01T23:00:00.000Z",
        fee=0.14,
        quantity=2.06331,
        symbol="KO",
        type="DIVIDEND",
        unit_price=0.46,
    ),
]


def get_ghostfolio_authorization_header() -> dict[str, str]:
    try:
        response = requests.post(
            f"{Settings.Ghostfolio.BASE_URL}/auth/anonymous",
            data={"accessToken": Settings.Ghostfolio.ACCOUNT_TOKEN},
        )
        response.raise_for_status()
        response_data = response.json()
        return {"Authorization": f"Bearer {response_data['authToken']}"}

    except requests.exceptions.HTTPError as ex:
        raise Exception(f"Error while authenticating with Ghostfolio: {ex}")


ghostfolio_authorization_header = get_ghostfolio_authorization_header()


def export_activities_to_ghostfolio(activities: list[GhostfolioActivity]) -> None:
    activities = list(map(lambda x: x.dict(by_alias=True), activities))

    data = {"activities": activities}

    response = requests.post(
        f"{Settings.Ghostfolio.BASE_URL}/import",
        headers=ghostfolio_authorization_header,
        json=data,
    )

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError as ex:
        raise Exception(f"Error while inserting new activities in Ghostfolio: {ex}")


for activity in activities:
    activity.comment = "Activity created by Tastytrade-Ghostfolio."

print("Started exporting activities to Ghostfolio...")
export_activities_to_ghostfolio(activities)
print("Done!")
