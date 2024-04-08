import sqlite3


class Db:
    def __init__(self, db_name="freelance.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.isolation_level = None  # Автоматически фиксируем изменения
        self.cursor = self.connection.cursor()
        self.connection.execute('pragma foreign_keys=ON')

    def create_table_user(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    sity TEXT,
                    age REAL,
                    experience TEXT,
                    sites TEXT,
                    mood TEXT,
                    otziv TEXT,
                    level REAL,
                    info_user TEXT
    );
""")
            print("[INFO] Table kod created successfully")

    def create_table_sale(self):
        with self.connection:
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS profiles (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            username TEXT,
                            business_niche TEXT,
                            city TEXT,
                            platforms TEXT,
                            expertise_level TEXT,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE   
            );
        """)
            print("[INFO] Table sale created successfully")

    def create_table_reviews(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    positive_reviews INTEGER,
                    negative_reviews INTEGER,
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("[INFO] Table reviews created successfully")

    def user_add(self, username, sity, age, experience, sites, mood, otziv, level, info_user):
        with self.connection:
            self.cursor.execute("INSERT INTO users (username, sity, age,experience, sites,mood,otziv,level, "
                                "info_user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (username, sity, age, experience, sites, mood, otziv, level, info_user))
            self.connection.commit()

    def check_username_exists(self, username):
        with self.connection:
            self.cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)", (username,))
            exists = self.cursor.fetchone()[0]
            return exists

    def insert_profile_data(self, user_id, username, business_niche, city, platforms, expertise_level):
        with self.connection:
            self.cursor.execute("""
                INSERT INTO profiles (user_id, username, business_niche, city, platforms, expertise_level)
                VALUES (?, ?, ?, ?, ?,?)
            """, (user_id, username, business_niche, city, platforms, expertise_level))
            print("[INFO] Profile data inserted successfully")

    def get_user_id_by_username(self, username):
        with self.connection:
            self.cursor.execute("""
                SELECT id FROM users WHERE username = ?
            """, (username,))
            result = self.cursor.fetchone()
            if result:
                return result[0]  # Возвращаем id пользователя, если найден
            else:
                return None

    def get_similar_profiles_by_city(self, city):
        with self.connection:
            self.cursor.execute("""
                SELECT * FROM profiles WHERE city LIKE ?
            """, ('%' + city + '%',))
            similar_profiles = self.cursor.fetchall()
            print(similar_profiles)
            return similar_profiles


    def get_sity_by_username(self, username):
        with self.connection:
            self.cursor.execute("""
                SELECT sity FROM users WHERE username = ?
            """, (username,))
            result = self.cursor.fetchone()
            print(result)
            return result

    def get_city_by_username(self, username):
        with self.connection:
            self.cursor.execute("""
                SELECT profiles.city
                FROM profiles
                INNER JOIN users ON profiles.user_id = users.id
                WHERE users.username = ?
            """, (username,))
            result = self.cursor.fetchone()
            print(result)
            if result:
                return result[0]  # Возвращаем city, если найден пользователь
            else:
                return None

    def delete_user_by_username(self, username):
        with self.connection:
            self.cursor.execute("""
                DELETE FROM users WHERE username = ?
            """, (username,))
            self.connection.commit()
            print("User with username {} deleted successfully.".format(username))


db = Db()
# db.create_table_sale()
# db.create_table_user()
# db.create_table_reviews()
# db.insert_profile_data(0, 'kk', 'kazan', 'yandex', '5')
# db.get_similar_profiles_by_city('kazan')
# db.get_sity_by_username('kkkostya666')
# db.get_city_by_username('kkkostya666')