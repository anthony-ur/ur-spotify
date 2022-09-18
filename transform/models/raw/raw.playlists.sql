{{ config(
    alias = 'playlist',
    enabled = false
) }}

select
   *
from {{ source('spotify', 'playlist') }}