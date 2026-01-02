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



