def tie_less_games(n, set_of_scores, game_so_far = []):
    """
    In rugby (union), a scoring event can give 3, 5 or 7 points.
    For kicks/penalties, 3 points are awarded, for unconverted tries 5 points
    and for converted tries 7 points. A game is a list of members of
    {-7,-5,-3,3,5,7} with negative points for the away team, positive for the
    home team.
    A tie-less game is one in which the teams never have the same score
    (except at the beginning, when no team has scored yet).
    This function determines how many games with n scoring events are tie-less
    """
    if n == len(game_so_far):
        return 1

    count = 0
    for score in set_of_scores:
        game_so_far.append(score)
        if sum(game_so_far) != 0:
            count += tie_less_games(n, set_of_scores, game_so_far)
        game_so_far.pop()
    return count

i = 0
while True:
    print('Tie-less rugby games with {} scoring events: {}'.format(
    i, tie_less_games(i, {3,5,7,-3,-5,-7})
    ))
    i += 1
# print([tie_less_games(i, {3,5,7,-3,-5,-7}) for i in range(5)])
# Rugby union: [1, 6, 30, 180, 1002, 6012, 34224, 205344, 1180010, 7080060, 40911324, 245467944]
