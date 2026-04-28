/* **************************************************************************************************** */
-- BioCatch Risk & Genuine Factors
-- Analiza los Factores de Riesgo detectados en el periodo seleccionado.
/* **************************************************************************************************** */

-- Set the schema; replace [db_name] with your schema name
use schema [db_name];

select   rf.key as risk_factor
        ,case when a.csid in (select f.csid from fraud_sessions f) then 'Fraud' else 'Non-Fraud' end as fraud_status
        ,hll(a.csid) as session_count
from     sessions a, lateral flatten (a.risk_factors) rf
where    rf.value::boolean = true
and      a.session_start_time between '{data_from}' and '{date_end}'
and      a.uid not like 'no_uid%'
group by risk_factor
        ,fraud_status
order by fraud_status, session_count desc
;
