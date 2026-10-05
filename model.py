import psycopg2

class Model:

    def __init__(self):
        self.db_config = {
            "dbname": "postgres",
            "user": "postgres",
            "password": "",
            "host": "localhost",
            "port": 5432,
        }

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def check_user_login(self, username, password):
        query = "SELECT id, username, full_name FROM users WHERE username = %s AND password = %s"
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (username, password))
                    return cur.fetchone()
        except Exception:
            return None

    def insert_full_record(self, user_id, plot_name, plot_loc, plant_name, plant_type, soil_type, ph, temp, humidity, notes):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO plots (plot_number, location) VALUES (%s, %s) RETURNING id;", (plot_name, plot_loc))
                plot_id = cur.fetchone()[0]

                cur.execute("INSERT INTO plants (plant_name, plant_type) VALUES (%s, %s) RETURNING id;", (plant_name, plant_type))
                plant_id = cur.fetchone()[0]

                cur.execute("INSERT INTO environment_data (soil_type, ph_level, temperature, humidity) VALUES (%s, %s, %s, %s) RETURNING id;", (soil_type, ph, temp, humidity))
                env_id = cur.fetchone()[0]

                cur.execute("INSERT INTO records (record_date, user_id, plot_id, plant_id, env_id, notes) VALUES (CURRENT_DATE, %s, %s, %s, %s, %s);", (user_id, plot_id, plant_id, env_id, notes))
            conn.commit()

    def update_record(self, record_id, plot_name, plot_loc, plant_name, plant_type, soil_type, ph, temp, humidity, notes):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT plot_id, plant_id, env_id FROM records WHERE id = %s", (record_id,))
                fk_data = cur.fetchone()
                if not fk_data:
                    raise Exception("Record not found")

                plot_id, plant_id, env_id = fk_data

                cur.execute("UPDATE plots SET plot_number = %s, location = %s WHERE id = %s", (plot_name, plot_loc, plot_id))
                cur.execute("UPDATE plants SET plant_name = %s, plant_type = %s WHERE id = %s", (plant_name, plant_type, plant_id))
                cur.execute("UPDATE environment_data SET soil_type = %s, ph_level = %s, temperature = %s, humidity = %s WHERE id = %s", (soil_type, ph, temp, humidity, env_id))
                cur.execute("UPDATE records SET notes = %s WHERE id = %s", (notes, record_id))
            conn.commit()

    def delete_record(self, record_id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM records WHERE id = %s;", (record_id,))
            conn.commit()

    def load_table_data(self):
        query = """
        SELECT 
            r.id,
            r.record_date,
            p.plot_number,
            p.location,
            pl.plant_name,
            pl.plant_type,
            e.soil_type,
            e.ph_level,
            e.temperature,
            e.humidity,
            r.notes
        FROM records r
        LEFT JOIN plots p ON r.plot_id = p.id
        LEFT JOIN plants pl ON r.plant_id = pl.id
        LEFT JOIN environment_data e ON r.env_id = e.id
        ORDER BY r.id DESC;
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    return cur.fetchall()
        except Exception:
            return []
