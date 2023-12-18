import json
from pprint import pprint

import requests
from tastytrade import Account, ProductionSession
from tastytrade.account import Transaction

from tastytrade_ghostfolio.adapters.ghostfolio_activity import adapt_activities
from tastytrade_ghostfolio.adapters.trade import adapt_trades
from tastytrade_ghostfolio.configs.settings import Settings
from tastytrade_ghostfolio.models.ghostfolio_activity import GhostfolioActivity


def get_tastytrade_session() -> ProductionSession:
    return ProductionSession(Settings.Tastytrade.USERNAME, Settings.Tastytrade.PASSWORD)


def get_tastytrade_account_history(session: ProductionSession) -> list[Transaction]:
    account = Account.get_accounts(session)[0]
    return account.get_history(session)


def filter_trades(transactions: list[Transaction]) -> list[Transaction]:
    trades = []
    for transaction in transactions:
        if transaction.transaction_type == "Trade" or (
            transaction.transaction_type == "Receive Deliver"
            and transaction.transaction_sub_type == "Dividend"
        ):
            trades.append(transaction)

    return trades


# def filter_dividends(transactions: list[Transaction]) -> list[Transaction]:
#     dividends = []
#     for transaction in transactions:
#         if (
#             transaction.transaction_sub_type == "Dividend"
#             and transaction.transaction_type == "Money Movement"
#         ):
#             dividends.append(transaction)

#     return dividends


# def extract_activities_from_account(
#     activities, account_id: str
# ) -> list[GhostfolioActivity]:
#     activities = list(filter(lambda x: x["accountId"] == account_id, activities))
#     return list(map(lambda x: GhostfolioActivity(**x), activities))


# response = requests.get(
#     f"{Settings.Ghostfolio.BASE_URL}/export",
#     headers={"Authorization": bearer_token},
# )
# response_data = response.json()
# accounts = response_data.get("accounts")
# tastytrade_account = next(
#     filter(lambda x: x["name"].lower() in ["tastyworks", "tastytrade"], accounts)
# )
# # activities = extract_activities_from_account(
# # response_data["activities"], tastytrade_account["id"]
# # )


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


def export_activities_to_ghostfolio(activities: list[GhostfolioActivity]) -> None:
    activities = adapt_activities(activities)

    data = {"activities": activities}

    response = requests.post(
        f"{Settings.Ghostfolio.BASE_URL}/import",
        headers=ghostfolio_authorization_header,
        json=data,
    )

    try:
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        raise Exception(
            f"Error while inserting new activities in Ghostfolio: {response.json()}"
        )


session = get_tastytrade_session()
transactions = get_tastytrade_account_history(session)

trades = filter_trades(transactions)
activities = adapt_trades(trades)

for activity in activities:
    activity.comment = "Activity created by Tastytrade-Ghostfolio."

ghostfolio_authorization_header = get_ghostfolio_authorization_header()
print("Started exporting activities to Ghostfolio...")
export_activities_to_ghostfolio(activities)
print("Done!")
