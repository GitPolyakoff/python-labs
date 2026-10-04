CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- 1 ко М с клиентами
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    balance REAL NOT NULL CHECK (balance >= 0),
    status TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients (id)
);

-- доп банковские услуг
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    fee REAL NOT NULL
);

-- доп таблица для связи М ко М
CREATE TABLE IF NOT EXISTS account_services (
    account_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    PRIMARY KEY (account_id, service_id),
    FOREIGN KEY (account_id) REFERENCES accounts (id),
    FOREIGN KEY (service_id) REFERENCES services (id)
);

CREATE INDEX IF NOT EXISTS idx_accounts_client ON accounts(client_id);
CREATE INDEX IF NOT EXISTS idx_clients_email ON clients(email);