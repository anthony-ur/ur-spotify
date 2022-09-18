{{ config(alias='track') }}

WITH raw_track AS (
    SELECT *
    FROM {{ source('spotify', 'track') }}
),
final as (
select     
    track_id,
    name,
    track_json[0]->>'duration_ms' as duration_ms,
    track_json[0]->>'key' as key,
    track_json[0]->>'mode' as mode,
    track_json[0]->>'tempo' as tempo,
    track_json[0]->>'energy' as energy,
    track_json[0]->>'liveness' as liveness,
    track_json[0]->>'loudness' as loudness,
    track_json[0]->>'speechiness' as speechiness,
    track_json[0]->>'acousticness' as acousticness,
    track_json[0]->>'danceability' as danceability,
    track_json[0]->>'time_signature' as time_signature,
    track_json[0]->>'instrumentalness' as instrumentalness 
from raw_track 
)
SELECT *
FROM final