# Разработка ML-сервиса на Python

Гурциев Ричард Зурабович  
Проект YanixTrade


<!-- ## Задания
1. Решение задачи компьютерного зрения (см. ветку [hw_1](https://github.com/vilovnok/image_itmo_course/tree/hw_1))
2. Решение задачи anomaly detection (см. ветку [hw_2](https://github.com/vilovnok/image_itmo_course/tree/hw_2))
4. Разные виды дистилляции (см. ветку [hw_4](https://github.com/vilovnok/image_itmo_course/tree/hw_4)) -->



CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    user_id INT,
    balance DECIMAL(10, 2) DEFAULT 500,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


INSERT INTO users (username)
VALUES ('r1char9');

INSERT INTO account (user_id) VALUES (1);


docker exec -it d2a66487c777 psql -U postgres -d yanix


BackLogger

1) Посмотреть на code в Verify services, а именно на schemes
Как бы VerifyCreate и VerifyCreateV2 ?