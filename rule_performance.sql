/* **************************************************************************************************** */
-- BioCatch Rule Performance Metrics
-- Analiza el rendimiento de las reglas en producción en un periodo determinado.
/* **************************************************************************************************** */

-- Set the schema; replace [db_name] with your schema name
use schema [db_name];

select   pm.value:rule_name::string as rule_name
        ,pm.value:status::string as rule_status
        ,a.score
        ,to_date(min(session_start_time)) as min_date
        ,to_date(max(session_start_time)) as max_date
        ,hll(a.csid) as session_count
        ,hll(case when a.csid in (select f.csid from fraud_sessions f) then a.csid end) as fraud_session_count
        ,hll(a.uid) as user_count
        ,hll(case when a.csid in (select f.csid from fraud_sessions f) then a.uid end) as fraud_user_count
        ,concat(
            round(div0(
                (hll(a.csid) - hll(case when a.csid in (select f.csid from fraud_sessions f) then a.csid end))
                ,hll(case when a.csid in (select f.csid from fraud_sessions f) then a.csid end)), 1)
            , ' :1') as gen_to_fraud_ratio
from     sessions a, lateral flatten(a.score_rules_results) pm
where    pm.value:status::string = 'production'
and      a.session_start_time between '{data_from}' and '{date_end}'
and      pm.value:triggered::boolean = true
group by rule_name
        ,rule_status
        ,score
;
