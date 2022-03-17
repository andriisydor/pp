CREATE TABLE user (
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(200),
	password VARCHAR(200),
	email VARCHAR(200),
    PRIMARY KEY (id)
);

CREATE TABLE song (
	id INT AUTO_INCREMENT,
	name VARCHAR(200) NOT NULL,
	singer VARCHAR(200),
    album VARCHAR(200),
    duration VARCHAR(200) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE playlist (
	id INT AUTO_INCREMENT,
	title VARCHAR(200),
    private BOOLEAN,
    user_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE playlist_song (
    playlist_id INT,
    song_id INT,
    FOREIGN KEY (playlist_id) REFERENCES playlist(id),
    FOREIGN KEY (song_id) REFERENCES song(id)
);