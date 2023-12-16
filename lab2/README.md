### Языки программирования и продукты на них

Бекенд написан на Python с использованием Flask. База данных - MySQL. Фронтенд - HTML с небольшими CSS стилями и скриптами на JavaScript.

Схема базы данных:

```
CREATE TABLE programming_languages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATE,
    rank INT
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    created_at DATE,
    user_count BIGINT,
    programming_language_id INT,
    FOREIGN KEY (programming_language_id) REFERENCES programming_languages(id)
);
```

Ранк - место в рейтинге согласно статье https://habr.com/ru/articles/730954/
Продукты компаний взял отсюда: https://rigorousthemes.com/blog/best-programming-software-examples/

## Некоторый функционал
 - Сортировка по столбцам при нажатии на них
 - Поиск в любой колонке + комбинированный поиск (можно сразу в двух искать)
 - Можно переходить к языку программирования продукта при нажатии на него
