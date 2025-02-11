CREATE TABLE IF NOT EXISTS allusers (
	userid VARCHAR(32) NOT NULL UNIQUE,
	phoneno BIGINT PRIMARY KEY,
	password VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
	productid int generated by default as identity
	(start with 1 increment by 1) primary key,
	sellerid varchar(32) not null,
	name varchar(64) not null,
	description varchar(256) not null,
	price money not null,
	category varchar(32) constraint category CHECK(category = 'dessert' OR category='ready meals' OR category = 'pastries' OR category = 'drinks'),
	allergen varchar(32) not null,
	minorder int not null check(minorder>=0),
	foreign key(sellerid) references allusers(userid)
);

CREATE TABLE IF NOT EXISTS transactions (
	orderid int generated by default as identity
	(start with 1 increment by 1),
	b_id varchar(32) not null,
	s_id varchar(32) not null,
	primary key(orderid, b_id, s_id),
	p_id int references products(productid) generated by default as identity
	(start with 1 increment by 1) unique,
	qty int not null check(qty>0),
	delivery varchar(12) not null check(delivery='self pickup' OR delivery='delivery'),
	status varchar(10) not null check(status='pending' OR status='approved'),
	foreign key(b_id) references allusers(userid),
	foreign key(s_id) references allusers(userid),
	check(not b_id = s_id)
);

CREATE TABLE IF NOT EXISTS buyers (
	b_id varchar(32) primary key
);

CREATE OR REPLACE FUNCTION new_buyer()
RETURNS trigger AS $$
BEGIN
	INSERT INTO buyers(b_id)
	VALUES(NEW.b_id) ON CONFLICT DO NOTHING;
 
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER update_buyers
AFTER INSERT
ON transactions
FOR EACH ROW
EXECUTE PROCEDURE new_buyer();

CREATE TABLE IF NOT EXISTS sellers (
	s_id varchar(32) primary key
);

CREATE OR REPLACE FUNCTION new_seller()
RETURNS trigger AS $$
BEGIN
	INSERT INTO sellers(s_id)
	VALUES(NEW.sellerid) ON CONFLICT DO NOTHING;
 
    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER update_sellers
AFTER INSERT
ON products
FOR EACH ROW
EXECUTE PROCEDURE new_seller();

CREATE OR REPLACE FUNCTION status_check()
RETURNS trigger AS $$

DECLARE 
	total_amount INT;
	minorder INT;

BEGIN
    SELECT SUM(qty) FROM transactions WHERE p_id = NEW.p_id INTO total_amount;
	SELECT minorder 
	FROM products
	WHERE productid = NEW.p_id;
    IF total_amount >= minorder THEN 
	UPDATE transactions SET status = 'approved' WHERE p_id = NEW.p_id;
	RETURN NEW;
	END IF;
	RETURN NULL;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER check_status
AFTER INSERT
ON transactions
FOR EACH ROW
EXECUTE PROCEDURE status_check();

/*
CREATE TABLE IF NOT EXISTS reviews (
	userid VARCHAR(32) REFERENCES transactions(b_id) NOT NULL UNIQUE,
	rated_p_id INT REFERENCES transactions(p_id) GENERATED BY DEFAULT AS IDENTITY
	(START WITH 1 INCREMENT BY 1),
	status VARCHAR(10) CONSTRAINT status CHECK (status = 'approved'),
	userrating INT CONSTRAINT userrating CHECK (userrating BETWEEN 0 AND 5),
	userreview VARCHAR(256),
	ratingdate DATE
);
*/

