# Ejemplos de Queries para Snowflake

Este archivo contiene ejemplos de consultas SQL que pueden ser utilizadas como base para el script de exportación. Recuerda que puedes reemplazar los filtros de fecha fijos por los tokens `{data_from}` y `{date_end}` para que el script los gestione dinámicamente.

---

## 1. BioCatch Score Distribution Queries
*Analiza la distribución del BioCatch Risk Score.*

```sql
/* **************************************************************************************************** */
-- BioCatch Score Distribution Queries
-- Authors: BioCatch Threat Analytics

-- These are query examples that analyze the score distribution of the BioCatch Risk Score
/* **************************************************************************************************** */

-- Set the schema; replace [db_name] with your schema name
use schema [db_name];

/* Overall Score Distribution */
-- Calculated over the last 30 days
-- To see more options for date/time, refer to:
-- -https://docs.snowflake.com/en/sql-reference/functions-date-time.html

select   floor(score / 100) * 100 as score_bin_100
        ,hll(csid) as session_count
        ,ratio_to_report(hll(csid)) over() as session_fraction
from     sessions_events
where    dateadd(day, -30, current_timestamp()) < session_start_time
and      uid not like 'no_uid%' -- Required for Account Takeover sessions (valid uid)
and      source = 'terminate_session' -- for getScore API, change source to getscore
group by score_bin_100
order by score_bin_100
;

/* Score Distribution, for getScore API, split by Fraud vs Non-fraud */
-- You can extend this query to include any other splits you would like to see by adding them to the select statement and the group by clause

select   case when csid in (select csid from fraud_sessions) then 'Fraud' else 'Non-fraud' end as fraud_status
        ,floor(score / 100) * 100 as score_bin_100
        ,hll(csid) as session_count
        ,ratio_to_report(hll(csid)) over(partition by fraud_status) as session_fraction
from     sessions_events
where    dateadd(day, -30, current_timestamp()) < session_start_time
and      uid not like 'no_uid%' -- Required for Account Takeover sessions (valid uid)
and      source = 'getscore'
and      score > 0 -- included to remove errors
group by fraud_status, score_bin_100
order by fraud_status, score_bin_100
;
```

---

## 2. BioCatch Rule Performance Metrics
*Analiza el rendimiento de las reglas en BioCatch Rule Manager.*

```sql
/* **************************************************************************************************** */
-- BioCatch Rule Performance Metrics
-- Authors: BioCatch Threat Analytics

-- These are query examples that analyze the performance of BioCatch Rule Manager rules
/* **************************************************************************************************** */

-- Set the schema; replace [db_name] with your schema name
use schema [db_name];

/* Production Rules - Score Override - Performance Summary Table */
-- Considers only rules that are set to Score Override
-- Calculated over the last 90 days
-- Includes only production rules

select   pm.value:rule_name::string as rule_name
        ,pm.value:status::string as rule_status
        ,a.score
        ,to_date(min(session_start_time)) as min_date -- will reflect the data period
        ,to_date(max(session_start_time)) as max_date -- will reflect the data period
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
where    pm.value:status::string = 'production' -- indicates rule is in production
and      dateadd(day, -90, current_timestamp()) < a.session_start_time -- You can change the number of days here
and      pm.value:triggered::boolean = true -- indicates rule fired and altered score
group by rule_name
        ,rule_status
        ,score
;

/* Evaluation Rules - Score Override - Performance Summary Table */
-- Considers only rules that are set to Score Override
-- Calculated over the last 90 days
-- Includes only evaluation rules

select   pm.value:rule_name::string as rule_name
        ,pm.value:status::string as rule_status
        ,to_date(min(session_start_time)) as min_date -- will reflect the data period
        ,to_date(max(session_start_time)) as max_date -- will reflect the data period
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
where    pm.value:status::string = 'evaluation' -- indicates rule is in evaluation
and      dateadd(day, -90, current_timestamp()) < a.session_start_time -- You can change the number of days here
and      pm.value:result::boolean = true -- indicates conditions of rules were met
group by rule_name
        ,rule_status
;

/* Rules - Alert - Performance Summary Table */
-- Considers only rules set to Alert
-- Calculated over the last 90 days
-- Includes only production rules

select   pm.value:rule_name::string as rule_name
        ,pm.value:status::string as rule_status
        ,to_date(min(session_start_time)) as min_date -- will reflect the data period
        ,to_date(max(session_start_time)) as max_date -- will reflect the data period
        ,hll(a.csid) as session_count
        ,hll(case when a.csid in (select f.csid from fraud_sessions f) then a.csid end) as fraud_session_count
        ,hll(a.uid) as user_count
        ,hll(case when a.csid in (select f.csid from fraud_sessions f) then a.uid end) as fraud_user_count
        ,concat(
            round(div0(
                (hll(a.csid) - hll(case when a.csid in (select f.csid from fraud_sessions f) then a.csid end))
                ,hll(case when a.csid in (select f.csid from fraud_sessions f) then a.csid end)), 1)
            , ' :1') as gen_to_fraud_ratio
from     sessions a, lateral flatten(a.alert_rules_results) pm
where    pm.value:status::string = 'production' -- indicates rule is in production
and      dateadd(day, -90, current_timestamp()) < a.session_start_time -- You can change the number of days here
and      pm.value:triggered::boolean = true -- indicates rule fired and an alert was sent
group by rule_name
        ,rule_status
;

/* Rules - Score Override - Daily Summary */
-- Checking production rules performance
-- Grouped by day to allow for further analysis

select   to_date(session_start_time) as day
        ,pm.value:rule_name::string as rule_name
        ,pm.value:status::string as rule_status
        ,a.score
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
where    pm.value:status::string = 'production'-- indicates rule is in production
and      dateadd(day, -90, current_timestamp()) < a.session_start_time -- You can change the number of days here
and      pm.value:triggered::boolean = true -- indicates rule fired and altered score
group by day
        ,rule_name
        ,rule_status
        ,score
;
```

---

## 3. BioCatch Risk & Genuine Factors
*Analiza los Factores de Riesgo y Genuinidad de BioCatch.*

```sql
/* **************************************************************************************************** */
-- BioCatch Risk & Genuine Factors
-- Authors: BioCatch Threat Analytics

-- These are query examples that analyze BioCatch Risk & Genuine Factors
/* **************************************************************************************************** */

-- Set the schema; replace [db_name] with your schema name
use schema [db_name];

/* Risk Factors Summary Table - Basic */
-- Counts of total session and fraud sessions that have a risk factor in the last 30 days

select   rf.key as risk_factor
        ,case when a.csid in (select f.csid from fraud_sessions f) then 'Fraud' else 'Non-Fraud' end as fraud_status
        ,hll(a.csid) as session_count
from     sessions a, lateral flatten (a.risk_factors) rf
where    rf.value::boolean = true
and      dateadd(day, -30, current_timestamp()) < a.session_start_time -- You can change the number of days here
and      a.uid not like 'no_uid%' -- Required for Account Takeover sessions (valid uid)
group by risk_factor
        ,fraud_status
order by fraud_status, session_count desc
;

/* Genuine Factors Summary Table - Basic */
-- Counts of total session and fraud sessions that have a risk factor in the last 30 days

select   gf.key as genuine_factor
        ,case when a.csid in (select f.csid from fraud_sessions f) then 'Fraud' else 'Non-Fraud' end as fraud_status
        ,hll(a.csid) as session_count
from     sessions a, lateral flatten (a.genuine_factors) gf
where    gf.value::boolean = true
and      dateadd(day, -30, current_timestamp()) < a.session_start_time -- You can change the number of days here
and      a.uid not like 'no_uid%' -- Required for Account Takeover sessions (valid uid)
group by genuine_factor
        ,fraud_status
order by fraud_status, session_count desc
;
```
