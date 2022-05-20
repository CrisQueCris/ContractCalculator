DROP TABLE IF EXISTS contracts;

CREATE TABLE contracts(
    contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
    commodity TEXT NOT NULL,
    date_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount_tonnes REAL NOT NULL,
    amount_euros REAL NOT NULL,
    date_fullfillment DATE NOT NULL
)