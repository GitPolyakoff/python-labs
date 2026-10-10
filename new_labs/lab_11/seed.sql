INSERT INTO clients (name, email) VALUES 
('Иван Иванов', 'ivan@mail.ru'),
('Анна Смирнова', 'anna@mail.ru'),
('Петр Петров', 'petr@mail.ru'),
('Елена Попова', 'elena@mail.ru'),
('Алексей Волков', 'alex@mail.ru');

INSERT INTO services (service_name, fee) VALUES 
('SMS информирование', 50.0),
('Премиум поддержка', 500.0),
('Страхование вкладов', 150.0);

INSERT INTO accounts (client_id, balance, status) VALUES 
(1, 15000.0, 'active'),
(1, 50000.0, 'active'),
(2, 3000.0, 'active'),
(2, 0.0, 'closed'),
(3, 120000.0, 'active'),
(3, 450.0, 'blocked'),
(4, 75000.0, 'active'),
(4, 100.0, 'active'),
(5, 90000.0, 'active'),
(5, 0.0, 'closed');

-- подключаю услуги к счетам (многие ко многим)
INSERT INTO account_services (account_id, service_id) VALUES 
(1, 1), (1, 2),
(3, 1),
(5, 2), (5, 3),
(7, 1);