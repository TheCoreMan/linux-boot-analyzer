ALTER TABLE "machines" DROP CONSTRAINT IF EXISTS "machines_fk0";

ALTER TABLE "collections" DROP CONSTRAINT IF EXISTS "collections_fk0";

ALTER TABLE "units" DROP CONSTRAINT IF EXISTS "units_fk0";

DROP TABLE IF EXISTS "machines";

DROP TABLE IF EXISTS "collections";

DROP TABLE IF EXISTS "collection to units";

DROP TABLE IF EXISTS "units";

