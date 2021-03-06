-- DROP TABLE uifwexp_facts;

CREATE TABLE public.uifwexp_facts
(
  demarcation_code text REFERENCES scorecard_geography (geo_code),
  financial_year integer,
  item_code text,
  item_label text,
  amount bigint,
  id serial,
  CONSTRAINT uifwexp_facts_pkey PRIMARY KEY (id),
  CONSTRAINT uifwexp_facts_unique_demarcation_financial_year_item UNIQUE (demarcation_code, financial_year, item_code)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.uifwexp_facts
  OWNER TO municipal_finance;
