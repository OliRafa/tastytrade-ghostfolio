from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class GhostfolioSettings:
    BASE_URL = f"{getenv('GHOSTFOLIO_BASE_URL')}/api/v1"
    ACCOUNT_TOKEN = getenv("GHOSTFOLIO_ACCOUNT_TOKEN")


class TastytradeSettings:
    USERNAME = getenv("TASTYTRADE_USERNAME")
    PASSWORD = getenv("TASTYTRADE_PASSWORD")


class Settings(GhostfolioSettings, TastytradeSettings):
    Ghostfolio = GhostfolioSettings
    Tastytrade = TastytradeSettings
