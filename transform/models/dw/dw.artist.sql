{{ config(alias='artist', enbaled=false) }}

WITH playlist_track_artist AS (
    SELECT *
    FROM {{ ref('prep.playlist_track_artist') }}
),
playlist_track as (
    select * 
    FROM {{ ref('ingest.playlist_track') }}
),
track as (
    select * 
    FROM {{ ref('ingest.track') }}
),
final as (
    select 
    distinct playlist_track_artist.artist_name,
    round(AVG(track.key),2) as avg_key,
    round(AVG(track.mode),2) as avg_mode,
    round(AVG(track.tempo),2) as avg_tempo,
    round(AVG(track.energy),2) as avg_energy,
    round(AVG(track.liveness),2) as avg_liveness,
    round(AVG(track.loudness),2) as avg_loudness,
    round(AVG(track.speechiness),2) as avg_speechiness,
    round(AVG(track.acousticness),2) as avg_acousticness,
    round(AVG(track.danceability),2) as avg_danceability,
    round(AVG(track.time_signature),2) as avg_time_signature,
    round(AVG(track.instrumentalness),2) as avg_instrumentalness,
    round(avg(track.duration_ms/1000)/60,1) as duration_minues,
    min(playlist_track.added_at)::date as min_track_added_on,
    max(playlist_track.added_at)::date as max_track_added_on,
    count(distinct playlist_track.playlist_id) as count_playlist,
    round(avg(track.duration_ms/1000)/60,1) as avg_track_duration_minutes
    from 
    playlist_track_artist
        join playlist_track on playlist_track_artist.playlist_id = playlist_track.playlist_id
        join track on playlist_track.track_id = track.track_id
    group by 1

)
select * from final