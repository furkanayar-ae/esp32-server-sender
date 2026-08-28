import sqlite3
import os

class LocalDatabase:
    def __init__(self, db_name="mes_database.db"):
        self.db_name = db_name
        self._create_tables()

    def _connect(self):
        """SQLite veritabanına bağlantı açar"""
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        """Uygulama ilk çalıştığında veritabanı tablosunu otomatik oluşturur"""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS production_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    station_id TEXT NOT NULL,
                    product_id TEXT NOT NULL,
                    operator_id TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_production(self, production_data):
        """Use Case'den gelen doğrulanmış veriyi local DB'ye kaydeder"""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO production_logs (station_id, product_id, operator_id, temperature, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                production_data.station_id,
                production_data.product_id,
                production_data.operator_id,
                production_data.temperature,
                production_data.status
            ))
            conn.commit()