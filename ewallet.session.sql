CREATE TABLE accounts(
    acc_id SERIAL PRIMARY KEY,
    acc_name VARCHAR(255) not null,
    balance NUMERIC CHECK(balance>=0),
    email TEXT UNIQUE not null,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

DROP table accounts;


CREATE TABLE transactions(
    td_id BIGSERIAL PRIMARY KEY,
    acc_id integer NOT NULL references accounts(acc_id),
    amount numeric NOT NULL CHECK (amount>0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO accounts (acc_name, balance, email)
VALUES
    ('Achal', 1200, 'achal@gmailcom'),
    ('Neha', 850, 'Neha@example.com'),
    ('Priya', 3000, 'Priya@example.com');

select * from accounts



INSERT INTO transactions(
    acc_id,amount
)VALUES(1,500);

select * from accounts

select * from transactions


//changing the table structure 
 drop table transactions;

CREATE TABLE transactions (
    tx_id BIGSERIAL PRIMARY KEY,
    from_acc_id INTEGER NOT NULL REFERENCES accounts(acc_id),
    to_acc_id INTEGER NOT NULL REFERENCES accounts(acc_id),
    amount NUMERIC NOT NULL CHECK (amount > 0), 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO transactions(from_acc_id,to_acc_id,amount)
VALUES(1,2,500)

//total money sent

SELECT a.acc_name,SUM()







