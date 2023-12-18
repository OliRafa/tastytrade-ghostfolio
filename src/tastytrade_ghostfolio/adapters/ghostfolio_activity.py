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
