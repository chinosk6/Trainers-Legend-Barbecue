PRAGMA foreign_keys = false;

CREATE TABLE IF NOT EXISTS "user" (
                        "uid" INTEGER PRIMARY KEY AUTOINCREMENT,
                        "name" TEXT NOT NULL,
                        "token" TEXT NOT NULL,
                        "permission" integer NOT NULL DEFAULT 0
);
UPDATE "sqlite_sequence" SET seq = 0 WHERE name = 'user';


CREATE TABLE IF NOT EXISTS "files" (
                         "filename" TEXT NOT NULL,
                         "hash" TEXT NOT NULL,
                         "updateTime" integer NOT NULL DEFAULT 0,
                         "updateUserId" INTEGER NOT NULL DEFAULT 0,
                         "description" TEXT NOT NULL DEFAULT 'no description'
);

PRAGMA foreign_keys = true;