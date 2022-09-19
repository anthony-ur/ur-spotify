{{ config(alias='track') }}

WITH raw_track AS (
    SELECT *
    FROM {{ source('spotify', 'track') }}
),
final as (
select     
    track_id,
    name,
    (track_json[0]->>'duration_ms')::numeric as duration_ms,
    ROUND((track_json[0]->>'key')::numeric,2) as key,
    ROUND((track_json[0]->>'mode')::numeric,2) as mode,
    ROUND((track_json[0]->>'tempo')::numeric,2) as tempo,
    ROUND((track_json[0]->>'energy')::numeric,2) as energy,
    ROUND((track_json[0]->>'liveness')::numeric,2) as liveness,
    ROUND((track_json[0]->>'loudness')::numeric,2) as loudness,
    ROUND((track_json[0]->>'speechiness')::numeric,2) as speechiness,
    ROUND((track_json[0]->>'acousticness')::numeric,2) as acousticness,
    ROUND((track_json[0]->>'danceability')::numeric,2) as danceability,
    ROUND((track_json[0]->>'time_signature')::numeric,2) as time_signature,
    ROUND((track_json[0]->>'instrumentalness')::numeric,2) as instrumentalness 
from raw_track 
)
SELECT *
FROM final