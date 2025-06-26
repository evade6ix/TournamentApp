def get_rank_from_elo(elo: int):
    if elo >= 1500:
        return {"tier": "Grand Master", "division": None}
    elif elo >= 1400:
        return {"tier": "Master", "division": "I"}
    elif elo >= 1350:
        return {"tier": "Master", "division": "II"}
    elif elo >= 1300:
        return {"tier": "Diamond", "division": "I"}
    elif elo >= 1250:
        return {"tier": "Diamond", "division": "II"}
    elif elo >= 1200:
        return {"tier": "Gold", "division": "I"}
    elif elo >= 1150:
        return {"tier": "Gold", "division": "II"}
    elif elo >= 1100:
        return {"tier": "Gold", "division": "III"}
    elif elo >= 1050:
        return {"tier": "Silver", "division": "I"}
    elif elo >= 1000:
        return {"tier": "Silver", "division": "II"}
    elif elo >= 950:
        return {"tier": "Silver", "division": "III"}
    elif elo >= 900:
        return {"tier": "Bronze", "division": "I"}
    elif elo >= 850:
        return {"tier": "Bronze", "division": "II"}
    else:
        return {"tier": "Bronze", "division": "III"}
