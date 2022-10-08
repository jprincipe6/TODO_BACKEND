Create TABLE MiniServer;

DROP TABLE relation;
DROP TABLE todos;
DROP TABLE tags;

CREATE TABLE IF NOT EXISTS todos(
    id INT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    completed BOOLEAN,
    order INT,
	url TEXT
)

CREATE TABLE IF NOT EXISTS tags(
    id INT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
	url TEXT
)


 CREATE TABLE IF NOT EXISTS relation(
    id_todo INT NOT NULL,
    id_tag INT NOT NULL,
    PRIMARY KEY(id_todo, id_tag),
    FOREIGN KEY(id_todo) REFERENCES todos(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(id_tag) REFERENCES tags(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

--select * from todos;
--select * from tags;
--select * from relation;

-- select * from todos;
-- select * from tags;
-- select * from relation;
-- DELETE FROM todos WHERE id in (6,7,8,9,10,11,12,13,14,15,16,17);

-- INSERT INTO
--	todos(id, title, completed, orden,url)
--	VALUES (1, 'build an API_1', FALSE, 1, null),
--	 (2, 'build an API_2', TRUE, 2,null),
--	 (3, 'build an API_3', FALSE, 3,null),
--	 (4, 'build an API_4', TRUE, 4,null),
--	 (5, 'build an API_5', FALSE, 5,null);

--INSERT INTO
	--tags(id, title,url)
	--VALUES (1, 'tags an API_1',null),
	 	   --(2, 'tags an API_2',null),
	 	  -- (3, 'tags an API_3',null),
	 	  -- (4, 'tags an API_4',null),
	      -- (5, 'tags an API_5',null);
