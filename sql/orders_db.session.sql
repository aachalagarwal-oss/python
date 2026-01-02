CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR not null
);

CREATE TABLE orders(
    order_id SERIAL PRIMARY KEY,
    order_name VARCHAR(255) ,
    order_price INT not null,
    user_id INT references users(user_id)

);

SELECT * FROM users INNER JOIN orders on users.user_id=orders.user_id

