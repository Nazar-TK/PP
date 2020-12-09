CREATE TABLE show (
show_id INT,
name TEXT NOT NULL,
show_type TEXT NOT NULL,
description TEXT NOT NULL,
time DATE NOT NULL,
place TEXT NOT NULL,
PRIMARY KEY(show_id)
);

CREATE TABLE users (
id INT,
name TEXT NOT NULL,
phone INT NOT NULL,
mail TEXT NOT NULL,
PRIMARY KEY(id)
);

CREATE TABLE ticket (
code INT,
is_avaliable TEXT NOT NULL,
clas TEXT NOT NULL,
show_ INT NOT NULL,
FOREIGN KEY (show_) REFERENCES show(show_id),
user_id INT,
FOREIGN KEY (user_id) REFERENCES users(id),
PRIMARY KEY(code)
);
