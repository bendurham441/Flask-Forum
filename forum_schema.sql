create table posts (
    id integer primary key autoincrement,
    title text not null,
    'text' not null
);

create table users (
    id integer primary key autoincrement,
    username text not null,
    password not null
);
