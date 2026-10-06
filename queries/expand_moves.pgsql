-- Expand moves to one move per row
SELECT
    id,
    m.ord,
    m.move
FROM
    chess_games g
    CROSS JOIN LATERAL jsonb_array_elements(g.moves)
WITH
    ORDINALITY AS m (
        move,
        ord
    );