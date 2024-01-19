import requests

from tastytrade_ghostfolio.adapters.ghostfolio_activity import (
    adapt_activities,
    adapt_activities_from_json,
)
from tastytrade_ghostfolio.configs.settings import GhostfolioSettings
from tastytrade_ghostfolio.models.ghostfolio_account import GhostfolioAccount
from tastytrade_ghostfolio.models.ghostfolio_activity import GhostfolioActivity


class GhostfolioService:
    def __init__(self) -> None:
        self.AUTHORIZATION_HEADER = self.get_ghostfolio_authorization_header()

    def get_ghostfolio_authorization_header(self) -> dict[str, str]:
        """Log in the user and get its authenticated header.

        Returns
        -------
        dict[str, str]
            The authenticated header to be used in requests.

        Raises
        ------
        Exception
            When an HTTP error occurred while authenticating the user.
        """
        try:
            response = requests.post(
                f"{GhostfolioSettings.BASE_URL}/auth/anonymous",
                data={"accessToken": GhostfolioSettings.ACCOUNT_TOKEN},
            )
            response.raise_for_status()
            response_data = response.json()
            return {"Authorization": f"Bearer {response_data['authToken']}"}

        except requests.exceptions.HTTPError as ex:
            raise Exception(f"Error while authenticating with Ghostfolio: {ex}")

    def get_all_orders(self, account_id: str | None = None) -> list[GhostfolioActivity]:
        """Get all orders for the logged in user.

        Otionally, the returned orders are filtered for a given `account_id`.

        Parameters
        ----------
        account_id : str | None, optional
            ID of a particular account to filter the orders by, by default None.

        Returns
        -------
        list[GhostfolioActivity]
            User's orders.

        Raises
        ------
        Exception
            When an HTTP error occurred while requesting the orders.
        """
        try:
            if account_id:
                query_parameters = {"accounts": account_id}

            else:
                query_parameters = None

            response = requests.get(
                f"{GhostfolioSettings.BASE_URL}/order",
                headers=self.AUTHORIZATION_HEADER,
                params=query_parameters,
            )
            response.raise_for_status()
            data = response.json()
            return adapt_activities_from_json(data["activities"])

        except requests.exceptions.HTTPError as ex:
            raise Exception(f"Error while requesting orders to Ghostfolio: {ex}")

    def export_activities_to_ghostfolio(self, activities: list[GhostfolioActivity]):
        """Insert all activities into Ghostfolio for a particular user and account.

        Parameters
        ----------
        activities : list[GhostfolioActivity]
            Activities to be inserted in a particular account.

        Raises
        ------
        Exception
            When an HTTP error occurred while inserting the activities.
        """
        activities = adapt_activities(activities)

        data = {"activities": activities}

        response = requests.post(
            f"{GhostfolioSettings.BASE_URL}/import",
            headers=self.AUTHORIZATION_HEADER,
            json=data,
        )

        try:
            response.raise_for_status()

        except requests.exceptions.HTTPError:
            raise Exception(
                f"Error while inserting new activities in Ghostfolio: {response.json()}"
            )

    def get_all_accounts(self) -> list[GhostfolioAccount]:
        """Get all accounts for the logged in user.

        Returns
        -------
        list[GhostfolioAccount]
            All accounts for the user.

        Raises
        ------
        Exception
            When an HTTP error occurred while fetching the accounts.
        """
        try:
            response = requests.get(
                f"{GhostfolioSettings.BASE_URL}/account",
                headers=self.AUTHORIZATION_HEADER,
            )
            response.raise_for_status()
            data = response.json()
            return [GhostfolioAccount(**account) for account in data["accounts"]]

        except requests.exceptions.HTTPError as ex:
            raise Exception(f"Error while requesting accounts to Ghostfolio: {ex}")

    def create_account(self, account: GhostfolioAccount) -> GhostfolioAccount:
        """Create a new account in Ghostfolio.

        Parameters
        ----------
        account : GhostfolioAccount
            Account parameters for creating a new account.

        Returns
        -------
        GhostfolioAccount
            The same account, now with the ID provided by Ghostfolio when creating.

        Raises
        ------
        Exception
            When the creation failed due to an HTTP error.
        """
        try:
            response = requests.post(
                f"{GhostfolioSettings.BASE_URL}/account",
                headers=self.AUTHORIZATION_HEADER,
                json=account.dict(by_alias=True),
            )
            response.raise_for_status()
            data = response.json()
            return GhostfolioAccount(**data)

        except requests.exceptions.HTTPError as ex:
            raise Exception(f"Error while requesting accounts to Ghostfolio: {ex}")
