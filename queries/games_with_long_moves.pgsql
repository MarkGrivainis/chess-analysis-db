-- Games that had long moves
SELECT
    *
FROM
    chess_games
WHERE
    moves @@ '$.time_spent > 10';