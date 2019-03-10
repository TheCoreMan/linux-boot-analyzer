CREATE TABLE "machines"
(
    "machine_id" bigint  NOT NULL,
    "hostname"   varchar NOT NULL,
    "version"    varchar NOT NULL,
    "system"     varchar NOT NULL,
    "node"       varchar NOT NULL,
    "release"    varchar NOT NULL,
    "machine"    varchar NOT NULL,
    "processor"  varchar NOT NULL,
    CONSTRAINT machines_pk PRIMARY KEY ("machine_id")
) WITH (
      OIDS= FALSE
    );



CREATE TABLE "collections"
(
    "collection_id" serial NOT NULL,
    "machine_id"    serial NOT NULL UNIQUE,
    "time"          TIME   NOT NULL,
    CONSTRAINT collections_pk PRIMARY KEY ("collection_id")
) WITH (
      OIDS= FALSE
    );



CREATE TABLE "collection to units"
(
    "collection_id" bigint NOT NULL UNIQUE,
    "unit_id"       bigint NOT NULL UNIQUE
) WITH (
      OIDS= FALSE
    );



CREATE TABLE "units"
(
    "unit_id"     serial  NOT NULL,
    "system"      varchar NOT NULL,
    "description" varchar NOT NULL,
    "user"        varchar,
    "group"       varchar,
    "image_path"  varchar,
    "image_hash"  varchar,
    "path"        varchar NOT NULL,
    "hash"        varchar NOT NULL,
    CONSTRAINT units_pk PRIMARY KEY ("unit_id")
) WITH (
      OIDS= FALSE
    );



ALTER TABLE "machines"
    ADD CONSTRAINT "machines_fk0" FOREIGN KEY ("machine_id") REFERENCES "collections" ("machine_id");

ALTER TABLE "collections"
    ADD CONSTRAINT "collections_fk0" FOREIGN KEY ("collection_id") REFERENCES "collection to units" ("collection_id");


ALTER TABLE "units"
    ADD CONSTRAINT "units_fk0" FOREIGN KEY ("unit_id") REFERENCES "collection to units" ("unit_id");

