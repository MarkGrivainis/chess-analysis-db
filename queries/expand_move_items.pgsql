SELECT
    id,
    move_num,
    turn,
    san
FROM
    chess_games,
    jsonb_to_recordset(moves) AS m (move_num SMALLINT, san TEXT, turn TEXT);