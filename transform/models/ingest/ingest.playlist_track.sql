{{ config(alias='playlist_track') }}

WITH raw_playlist_track AS (
    SELECT *
    FROM {{ source('spotify', 'playlist_track') }}
),
final as (
    select 
    playlist_id,
    track_id 
    from raw_playlist_track 
)
SELECT *
FROM final