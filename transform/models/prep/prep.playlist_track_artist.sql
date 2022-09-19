{{ config(alias='playlist_track_artist') }}

WITH raw_playlist_track AS (
    SELECT *
    FROM {{ source('spotify', 'playlist_track') }}
),
final as (
    select
    playlist_id,
    track_id,
    jsonb_array_elements_text(playlist_track_json->'track'->'artists') as artist_name
    from raw_playlist_track 
)
SELECT *
FROM final