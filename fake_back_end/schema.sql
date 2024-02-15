PRAGMA foreign_keys = ON;

CREATE TABLE input(
	constr VARCHAR(1000),
	dbname VARCHAR(100),
	collection VARCHAR(100),
	idField VARCHAR(100),
	docField VARCHAR(100),
	fetched BOOLEAN NOT NULL CHECK (fetched IN (0, 1))
);

CREATE TABLE documents(
	document_id VARCHAR(200) NOT NULL UNIQUE,
	context VARCHAR(10000),
	entity_fetched BOOLEAN NOT NULL CHECK (entity_fetched IN (0, 1)),
	PRIMARY KEY(document_id)
);

CREATE TABLE entities(
	document_id VARCHAR(200),
	context VARCHAR(100),
	startPos INT,
	endPos INT,
	label VARCHAR(100)
);

CREATE TABLE relations(
	relation_id VARCHAR(200) NOT NULL UNIQUE,
	entity_1 VARCHAR(200) NOT NULL,
	entity_2 VARCHAR(200) NOT NULL,
	relation VARCHAR(200) NOT NULL,
	confirmed INT DEFAULT 0,
	score FLOAT,
	PRIMARY KEY(relation_id)
);