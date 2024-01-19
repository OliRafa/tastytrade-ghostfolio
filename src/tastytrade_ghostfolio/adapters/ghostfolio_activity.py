from datetime import datetime

from tastytrade_ghostfolio.models.ghostfolio_activity import GhostfolioActivity


def adapt_activities(
    activities: list[GhostfolioActivity],
) -> list[dict[str, str | float]]:
    adapted_activities = []

    for activity in activities:
        adapted_activities.append(_adapt_activity(activity))

    return adapted_activities


def _adapt_activity(activity: GhostfolioActivity) -> dict[str, str | float]:
    activity = activity.dict(by_alias=True)
    activity["type"] = activity["type"].value
    activity["date"] = str(activity["date"])
    return activity


def adapt_activities_from_json(activities: list[dict]) -> list[GhostfolioActivity]:
    return [_adapt_activity_from_json(activity) for activity in activities]


def _adapt_activity_from_json(activity: dict) -> GhostfolioActivity:
    activity["date"] = datetime.strptime(activity["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    activity["currency"] = activity["SymbolProfile"]["currency"]
    activity["symbol"] = activity["SymbolProfile"]["symbol"]
    return GhostfolioActivity(**activity)
