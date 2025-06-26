def calculate_elo(p1_elo: int, p2_elo: int, winner: str, k: int = 32):
    # Calculate expected scores
    expected_p1 = 1 / (1 + 10 ** ((p2_elo - p1_elo) / 400))
    expected_p2 = 1 / (1 + 10 ** ((p1_elo - p2_elo) / 400))

    # Actual scores
    if winner == "player1":
        score_p1, score_p2 = 1, 0
    elif winner == "player2":
        score_p1, score_p2 = 0, 1
    else:
        raise ValueError("Winner must be 'player1' or 'player2'")

    # New ELOs
    new_p1 = round(p1_elo + k * (score_p1 - expected_p1))
    new_p2 = round(p2_elo + k * (score_p2 - expected_p2))

    return new_p1, new_p2
