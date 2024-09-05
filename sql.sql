CREATE TABLE public.products (
	id int GENERATED ALWAYS AS IDENTITY NOT NULL,
	id_producto int NOT NULL,
	clave varchar NOT NULL,
	categoria varchar NULL,
	descripcion_corta varchar NULL,
	existencia varchar NULL,
	precio float8 NULL,
	moneda varchar NULL,
	tipo_cambio float8 NULL,
	imagen_url varchar NULL,
	CONSTRAINT products_pk PRIMARY KEY (id)
);
