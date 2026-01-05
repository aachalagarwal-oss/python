CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR not null
);
DROP table users;


CREATE TABLE orders(
    order_id SERIAL PRIMARY KEY,
    order_name VARCHAR(255) ,
    order_price INT not null,
    user_id INT references users(user_id)

);

DROP table orders;

/*SELECT * FROM users INNER JOIN orders on users.user_id=orders.user_id//learning thejoin*/


INSERT INTO users(user_name) VALUES('Aachal')
INSERT INTO users(user_name) VALUES('Aachal'),('Neha'),('Priya'),('Rahul')


INSERT INTO orders  (order_name, order_price, user_id) VALUES('Dosa',100,1),('chowmin',250,1),('idli',350,2),('Noodles',400,3),('Dosa',100,4),('chowmin',250,4),('idli',350,3),('Noodles',400,2)



SELECT 
u.user_name ,sum(o.order_price) as total_spent
from users u
join orders o
on u.user_id=o.user_id
group by u.user_id
ORDER BY total_spent desc;

//2 different users as aachal so we r getting 2 times...the query is proper


//more queries to be done for pratise


select u.user_name,o.order_price,o.order_name
from users u JOIN orders o
on u.user_id=o.user_id


select user_name from users u left join orders o on u.user_id=o.user_id


select DISTINCT  u.user_name from users u join orders o on u.user_id=o.user_id


select * from users

select u.user_name ,count(o.order_id) as total_orders
from users u JOIN orders o 
on u.user_id=o.user_id
group by u.user_id


SELECT u.user_name , SUM(o.order_price) as total_spent
FROM users u JOIN orders o on u.user_id=o.user_id group by u.user_id having sum(o.order_price)>500



select u.user_name from users u left Join orders o on u.user_id=o.user_id where o.user_id is NULL




select user_name , SUM(o.order_price) as total_spent
from users u JOIN orders o on u.user_id=o.user_id group by u.user_id Order by total_spent asc;


select u.user_name,
    COUNT(o.order_id) as total_orders
from users u
    JOIN orders o on u.user_id = o.user_id
group by u.user_id
having count(o.order_id) > 2
//alias are cretaed after having



SELECT u.user_name,u.user_id, COUNT(*) 
FROM orders o join users u ON o.user_id = u.user_id
GROUP BY u.user_id;


