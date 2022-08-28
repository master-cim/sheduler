-- Table: public.action

-- DROP TABLE IF EXISTS public.action;

CREATE TABLE IF NOT EXISTS public.action
(
    name_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character(200) COLLATE pg_catalog."default",
    description character(200) COLLATE pg_catalog."default",
    time_start character(20) COLLATE pg_catalog."default",
    day_start date,
    class integer NOT NULL DEFAULT 1,
    CONSTRAINT action_pkey PRIMARY KEY (name_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.action
    OWNER to xgzvvjjrgtsatk;