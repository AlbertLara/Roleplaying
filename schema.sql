CREATE SCHEMA IF NOT EXISTS "sw";

create table IF NOT EXISTS public."User"
(
    id serial PRIMARY KEY,
    email VARCHAR(60) UNIQUE NOT NULL,
    username VARCHAR(60) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    confirmed BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS public."Sistemas"
(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    sKey VARCHAR(10) UNIQUE NOT NULL,
    status VARCHAR(1) NOT NULL
);


CREATE TABLE IF NOT EXISTS public."Games"
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(40) UNIQUE NOT NULL,
    game_key VARCHAR(255) UNIQUE NOT NULL,
    max_players integer NOT NULL,
    masterId integer NOT NULL,
    sistema_Id integer,
    is_public BOOLEAN,
    creation_date TIMESTAMP NOT NULL,
    update_date TIMESTAMP NOT NULL,
    CONSTRAINT "Games_sistema_Id_fkey" FOREIGN KEY (sistema_Id)
        REFERENCES "Sistemas" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);


CREATE TABLE IF NOT EXISTS public."Members"
(
    id SERIAL PRIMARY KEY NOT NULL,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    approved BOOLEAN,
    CONSTRAINT "Members_game_id_fkey" FOREIGN KEY (game_id)
        REFERENCES "Games" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Members_user_id_fkey" FOREIGN KEY (user_id)
    REFERENCES "User" (id)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);


INSERT INTO "Sistemas" (nombre, sKey, status) VALUES ('Star Wars','SW','a');


CREATE TABLE IF NOT EXISTS "sw"."Razas"
(
    id SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    atributos VARCHAR(4) NOT NULL
);

CREATE TABLE IF NOT EXISTS "sw"."RazasAtributos"
(
    id SERIAL PRIMARY KEY NOT NULL,
    raza_id INTEGER NOT NULL,
    atributo VARCHAR(3) NOT NULL,
    val_min VARCHAR(3) NOT NULL,
    val_max VARCHAR(3) NOT NULL
);


CREATE TABLE IF NOT EXISTS "sw"."ListAtributos"
(
    id SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(30) UNIQUE NOT NULL,
    short_name VARCHAR(3) UNIQUE NOT NULL
);