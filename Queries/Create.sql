-- Table: public.datos_usuario_contacto

-- DROP TABLE IF EXISTS public.datos_usuario_contacto;

CREATE TABLE IF NOT EXISTS public.datos_usuario_contacto
(
    id integer NOT NULL DEFAULT nextval('datosusuarioscontacto_id_seq'::regclass),
    nombre character varying(100) COLLATE pg_catalog."default" NOT NULL,
    email character varying(50) COLLATE pg_catalog."default" NOT NULL,
    telefono character varying(50) COLLATE pg_catalog."default" NOT NULL,
    materia_interes character varying(30) COLLATE pg_catalog."default" NOT NULL,
    primaria boolean NOT NULL DEFAULT false,
    secundaria boolean NOT NULL DEFAULT false,
    terciario boolean NOT NULL DEFAULT false,
    universidad boolean NOT NULL DEFAULT false,
    mensaje character varying(150) COLLATE pg_catalog."default",
    fecha_solicitud_contacto date DEFAULT CURRENT_DATE,
    fecha_contacto_cliente date,
    CONSTRAINT datosusuarioscontacto_pkey PRIMARY KEY (id),
    CONSTRAINT nivel_materia CHECK (primaria IS TRUE AND secundaria IS FALSE AND terciario IS FALSE AND universidad IS FALSE OR primaria IS FALSE AND secundaria IS TRUE AND terciario IS FALSE AND universidad IS FALSE OR primaria IS FALSE AND secundaria IS FALSE AND terciario IS TRUE AND universidad IS FALSE OR primaria IS FALSE AND secundaria IS FALSE AND terciario IS FALSE AND universidad IS TRUE OR primaria IS FALSE AND secundaria IS FALSE AND terciario IS FALSE AND universidad IS FALSE)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.datos_usuario_contacto
    OWNER to postgres;