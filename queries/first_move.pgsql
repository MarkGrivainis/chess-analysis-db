-- Get the first move in every game
SELECT
    moves -> 0 ->> 'san'
FROM
    chess_games;