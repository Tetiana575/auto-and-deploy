import psycopg2  # type: ignore

class PGDatabase: # класс для работы с бд
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database  # Исправлено на правильное имя атрибута
        self.user = user
        self.password = password

        # Подключение к базе данных
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()  # получение курсора
        self.conn.autocommit = True  # автокоммит

    def post(self, query, args=()):  # функция для отправки запросов
        try:
            self.cur.execute(query, args)  # выполнение запроса
            self.conn.commit()  # коммит
        except Exception as err:  # обработка ошибок
            print("Ошибка при выполнении запроса:", repr(err))

    def fetch_all(self, query, args=()):  # функция для выборки всех записей
        try:
            self.cur.execute(query, args)  # выполнение запроса
            return self.cur.fetchall()  # возвращает все результаты
        except Exception as err:  # обработка ошибок
            print("Ошибка при выборке данных:", repr(err))
            return None

    def update(self, query, args=()):  # функция обновления данных
        self.post(query, args)  # переиспользуем метод post

    def delete(self, query, args=()):  # функция удаления данных
        self.post(query, args)  # переиспользуем метод post

    def close(self):  # функция закрытия соединения
        self.cur.close()  # закрываем курсор
        self.conn.close()  # закрываем соединение