WITH unnested_evals AS (
    SELECT 
        g.id AS game_id,
        m.ord AS move_number,
        m.move->>'san' AS san,
        m.move->>'color' AS color,
        m.move->>'stockfish_eval' AS raw_eval,
        -- Normalize regular numbers and 'm-6', 'm6', 'm+4' strings into a numeric score
        CASE 
            -- Check for mate string (starts with 'm' or 'M')
            WHEN (m.move->>'stockfish_eval') ~* '^m' THEN
                CASE 
                    -- Mate for Black (e.g., 'm-6')
                    WHEN (m.move->>'stockfish_eval') ~* '^m\s*-\d+' THEN
                        -10000 + abs((substring(m.move->>'stockfish_eval' from '-?\d+'))::numeric)
                    -- Mate for White (e.g., 'm4' or 'm+4')
                    ELSE
                        10000 - abs((substring(m.move->>'stockfish_eval' from '\d+'))::numeric)
                END
            -- Normal centipawn / pawn evaluations
            WHEN (m.move->>'stockfish_eval') ~ '^-?\d+(\.\d+)?$' THEN
                (m.move->>'stockfish_eval')::numeric
            ELSE NULL
        END AS current_eval
    FROM chess_games g
    CROSS JOIN LATERAL jsonb_array_elements(g.moves) WITH ORDINALITY AS m(move, ord)
),
eval_with_lag AS (
    SELECT 
        game_id,
        move_number,
        san,
        color,
        raw_eval,
        current_eval,
        LAG(current_eval) OVER (
            PARTITION BY game_id 
            ORDER BY move_number
        ) AS prev_eval,
        LAG(raw_eval) OVER (
            PARTITION BY game_id 
            ORDER BY move_number
        ) AS prev_raw_eval
    FROM unnested_evals
),
swings AS (
    SELECT 
        game_id,
        move_number,
        san,
        color,
        prev_raw_eval,
        raw_eval AS current_raw_eval,
        prev_eval,
        current_eval,
        ABS(current_eval - prev_eval) AS eval_delta,
        -- How much the player who just moved harmed their own evaluation
        CASE 
            WHEN color = 'white' THEN (prev_eval - current_eval)
            WHEN color = 'black' THEN (current_eval - prev_eval)
        END AS eval_lost
    FROM eval_with_lag
    WHERE prev_eval IS NOT NULL AND current_eval IS NOT NULL
)
SELECT 
    game_id,
    move_number,
    color,
    san,
    prev_raw_eval,
    current_raw_eval,
    eval_delta,
    eval_lost
FROM swings
-- 200cp swing or an outright mate transition
-- WHERE eval_delta >= 5
ORDER BY eval_delta DESC;