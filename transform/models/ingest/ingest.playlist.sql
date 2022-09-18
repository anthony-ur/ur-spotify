{{ config(alias='playlist') }}

WITH raw_playlist AS (
    SELECT *
    FROM {{ source('spotify', 'playlist') }}
),
final as (
select 
    playlist_id,
    playlist_json ->> 'uri' as uri,
    playlist_json ->> 'name' as name,
    playlist_json ->> 'description' as description 
from raw_playlist 
)
SELECT *
FROM final