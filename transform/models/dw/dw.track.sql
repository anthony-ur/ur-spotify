{{ config(alias='track') }}

WITH playlist AS (
    SELECT *
    FROM {{ ref('ingest.playlist') }}
),
track as (
    select * 
    FROM {{ ref('ingest.track') }}
),
playlist_track as (
    select * 
    FROM {{ ref('ingest.playlist_track') }}
),
final as (
    select 
    distinct track.track_id,
    track.name,
    track.key,
    track.mode,
    track.tempo,
    track.energy,
    track.liveness,
    track.loudness,
    track.speechiness,
    track.acousticness,
    track.danceability,
    track.time_signature,
    track.instrumentalness,
    round((track.duration_ms/1000)/60,1) as duration_minues,
    min(playlist_track.added_at)::date as min_track_added_on,
    max(playlist_track.added_at)::date as max_track_added_on,
    count(distinct playlist.playlist_id) as count_playlist,
    round(avg(track.duration_ms/1000)/60,1) as avg_track_duration_minutes
    from 
    playlist
        join playlist_track on playlist.playlist_id = playlist_track.playlist_id
        join track on playlist_track.track_id = track.track_id
    group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14
    #TODO: fix this ugly groupby lol
)
select * from final