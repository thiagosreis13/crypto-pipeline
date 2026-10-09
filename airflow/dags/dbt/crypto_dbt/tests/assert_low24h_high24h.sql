select 
    id, 
    last_updated,
    high_24h,
    low_24h
from {{ref('stg_top5_nova_versao')}}
where low_24h > high_24h