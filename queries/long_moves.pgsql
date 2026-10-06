-- Expand moves to one move per row and filter for long moves
SELECT
    id,
    m.ord,
    m.move,
    m.move -> 'time_spent'
FROM
    chess_games g
    CROSS JOIN LATERAL jsonb_array_elements(g.moves)
WITH
    ORDINALITY AS m (
        move,
        ord
    )
WHERE
    (m.move -> 'time_spent')::NUMERIC > 10;