create table public.user(
	id Serial ,
	username varchar,
	password varchar,
	email varchar,
	primary key(id)
);

create table public.song(
	id serial,
	name varchar not null,
	singer varchar,
	album varchar,
	duration varchar not null,
	primary key (id)
);

create table public.playlist(
	id Serial,
	title varchar,
	user_id integer,
	private boolean,
	primary key(id)
);

create table public.playlist_song(
	playlist_id integer ,
	song_id integer
);

ALTER TABLE public.playlist
    ADD FOREIGN KEY (user_id)
    REFERENCES public.user (id)
    NOT VALID;

ALTER TABLE public.playlist_song
    ADD FOREIGN KEY (playlist_id)
    REFERENCES public.playlist (id)
    NOT VALID;


ALTER TABLE playlist_song
    ADD FOREIGN KEY (song_id)
    REFERENCES song (id)
    NOT VALID;
