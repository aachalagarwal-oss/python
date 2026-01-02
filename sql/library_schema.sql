CREATE TABLE authors(
    author_id SERIAL PRIMARY KEY,
    name TEXT not null
);



 CREATE TABLE Book(
    book_id SERIAL PRIMARY KEY,
    book_title VARCHAR(255) not null,
    author_id INT references authors(author_id)
 );


 CREATE TABLE Categories(
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) not null
 );


 CREATE TABLE Book_categories(
    book_id INT references Book(book_id),
    category_id INT references Categories(category_id),
    PRIMARY KEY (book_id,category_id)
 );

 CREATE TABLE members(
    Member_id SERIAL PRIMARY KEY,
    email TEXT not null UNIQUE,
    name VARCHAR(255) not null,
    join_date DATE not null

 );


 ALTER TABLE book 
 ADD COLUMN isbn TEXT NOT NULL UNIQUE


 INSERT INTO authors (name)
VALUES ('Achal');

INSERT INTO book(book_title, isbn, author_id)
VALUES ('1984', '978-0451524935', 1);

INSERT INTO book (book_title, isbn, author_id)
VALUES ('The praise', '978', 2);//failed test

SELECT * from authors
SELECT * from book


INSERT INTO Categories (category_name)
VALUES ('Friction');


INSERT INTO Categories (category_name)
VALUES ('Horror');

SELECT * from categories

DELETE from categories
where category_id=2;//deleting the duplicate fricition category 2 

SELECT * from categories


INSERT INTO Book_categories( book_id,category_id)
VALUES(1,1)

INSERT INTO Book_categories( book_id,category_id)
VALUES(1,2)//failed as category 2 doesnt exist


INSERT INTO Book_categories( book_id,category_id)
VALUES(1,3)


SELECT * from book_categories


INSERT INTO Book_categories( book_id,category_id)
VALUES(3,3)

SELECT * from book_categories//here we can see many to many relationship








