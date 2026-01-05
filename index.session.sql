CREATE table users(
    user_id SERIAL PRIMARY KEY,
    user_name TEXT,
    email TEXT
)


INSERT INTO users(user_name,email)
SELECT
'user_' ||g,
'user' || g ||'@example.com'

FROM generate_series(1,1000000)g;//inswritn the data with function




CREATE INDEX idx_users_email

on USERS(email)


SELECT *
FROM users
WHERE email = 'user500000@example.com';//faster search


DROP INDEX idx_users_email


SELECT *
FROM users
WHERE email = 'user500000@example.com';//slow results but now runs faster becuse of cache