create table IF NOT EXISTS public."User"
(
    id serial PRIMARY KEY,
    email VARCHAR(60) UNIQUE NOT NULL,
    username VARCHAR(60) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL,
    active BOOLEAN NOT NULL,
    online BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS public."UserAtributes"
(
    id SERIAL PRIMARY KEY,
    userId INTEGER NOT NULL,
    Atribute_name VARCHAR(60) NOT NULL,
    Atribute_value VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS public."Group" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(40) UNIQUE NOT NULL,
    group_key VARCHAR(255) UNIQUE NOT NULL,
    max_players INTEGER NOT NULL,
    is_public BOOLEAN NOT NULL

);

CREATE TABLE IF NOT EXISTS public."Friends" (
    id SERIAL PRIMARY KEY NOT NULL,
    friend_a_id INTEGER NOT NULL,
    friend_b_id INTEGER NOT NULL,
    accepted BOOLEAN,
    CONSTRAINT "friend_a_fkey" FOREIGN KEY (friend_a_id)
        REFERENCES "User" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "friend_b_fkey" FOREIGN KEY (friend_b_id)
        REFERENCES "User" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);


CREATE TABLE IF NOT EXISTS public."Members"
(
    id SERIAL PRIMARY KEY NOT NULL,
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    approved BOOLEAN,
    role VARCHAR(6),
    CONSTRAINT "Members_group_id_fkey" FOREIGN KEY (group_id)
        REFERENCES "Group" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "Members_user_id_fkey" FOREIGN KEY (user_id)
    REFERENCES "User" (id)
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
);