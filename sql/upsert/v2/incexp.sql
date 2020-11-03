\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE incexp_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        function_code TEXT,
        item_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;
CREATE INDEX incexp_upsert_demarcation_code on incexp_upsert (demarcation_code);
CREATE INDEX incexp_upsert_period_code on incexp_upsert (period_code);

\echo Read data...

\copy incexp_upsert (demarcation_code, period_code, function_code, item_code, amount) FROM '/Users/juriejan/Downloads/openup/data/mscoa/incexp.csv' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM incexp_facts_mscoa f WHERE EXISTS (
        SELECT 1 FROM incexp_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO incexp_facts_mscoa
(
    demarcation_code,
    period_code,
    function_id,
    item_id,
    amount,
    financial_year,
    amount_type_id,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       (select id from government_functions_mscoa where government_functions_mscoa.code = function_code),
       (select id from incexp_items_mscoa where incexp_items_mscoa.code = item_code),
       amount,
       cast(left(period_code, 4) as int),
       case when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)(M\d{2})?$'
               then (select id from amount_type_mscoa where amount_type_mscoa.code = substr(period_code, 5, 4))
           when period_code ~ '^\d{4}M\d{2}$'
               then (select id from amount_type_mscoa where amount_type_mscoa.code = 'ACT')
       end,
       case when period_code ~ '^\d{4}(ADJB|ORGB)?M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}(ADJB|ORGB)?M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)$'
                then cast(left(period_code, 4) as int)
       end
FROM incexp_upsert i;

COMMIT;
