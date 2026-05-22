-- CREATE table produkty (
-- 	id INT auto_increment PRIMARY KEY,
--     nazev VARCHAR(100),
--     cena DECIMAL(10,2),
--     skladem INT
--     );
--     
-- insert into produkty(nazev, cena, skladem) VALUES
-- 	('mobilni telefon', 15000.00, 20),
--     ('notebook', 25000.00, 10),
--     ('sluchatka', 2500.00, 50);
    
-- select * from produkty;

    
-- CREATE table uzivatele (
-- 	id INT auto_increment PRIMARY KEY,
-- 	jmeno VARCHAR(100),
--     email VARCHAR(100)
--     );
--     

-- Create table objednavky (
-- 	id INT auto_increment PRIMARY KEY,
--     uzivatel_id INT,
--     datum date,
--     castka decimal,
-- 	FOREIGN KEY (uzivatel_id) REFERENCES uzivatele(id)
--     );
--     

-- insert into uzivatele(jmeno, email) VALUES
-- 	('Ondrej Rychly', 'o.rych@gmail.com'),
--     ('Martin Rychly', 'mrncz11111@gmail.com'),
--     ('Jura Byma', 'jiribyma@gmail.com'),
--     ('Marek Byma', 'marekbyms@gmail.com')

/*CREATE TABLE ukoly(
	id int auto_increment primary key,
    nazev varchar(100),
    popis varchar(200),
	stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') default 'Nezahájeno',
	datum_vytvoreni DATE
); 
*/






