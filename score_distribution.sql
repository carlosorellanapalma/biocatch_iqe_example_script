/* **************************************************************************************************** */
-- BioCatch Score Distribution Query
-- Analiza la distribución del BioCatch Risk Score entre dos fechas dadas.
/* **************************************************************************************************** */

-- Set the schema; replace [db_name] with your schema name
use schema [db_name];

select   floor(score / 100) * 100 as score_bin_100
        ,hll(csid) as session_count
        ,ratio_to_report(hll(csid)) over() as session_fraction
from     sessions_events
where    session_start_time between '{data_from}' and '{date_end}'
and      uid not like 'no_uid%' -- Required for Account Takeover sessions (valid uid)
and      source = 'terminate_session'
group by score_bin_100
order by score_bin_100
;
