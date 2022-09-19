{{ config(alias='playlist') }}

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
    distinct playlist.playlist_id,
    playlist.name,
    min(playlist_track.added_at)::date as min_track_created_on,
    max(playlist_track.added_at)::date as max_track_created_on,
    count(distinct track.track_id) as count_track,
    round(sum(track.duration_ms/1000)/60,1) as sum_duration_minutes,
    round(avg(track.duration_ms/1000)/60,1) as avg_track_duration_minutes
    from 
    playlist
        join playlist_track on playlist.playlist_id = playlist_track.playlist_id
        join track on playlist_track.track_id = track.track_id
    group by 1,2

)
select * from final