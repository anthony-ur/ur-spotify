{{ config(alias='playlist_track') }}

WITH raw_playlist_track AS (
    SELECT *
    FROM {{ source('spotify', 'playlist_track') }}
),
final as (
    select 
    playlist_id,
    track_id,
    (playlist_track_json->>'added_at')::timestamp as added_at 
    from raw_playlist_track 
)
SELECT *
FROM final