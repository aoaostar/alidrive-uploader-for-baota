import sqlite3

plugin_path = "/www/server/panel/plugin/aliyundrive_uploader/"
logs_dir = plugin_path + "logs"
db_file = plugin_path + "drive/db.db"


class aliyundrive_uploader_migrate():
    def __init__(self):
        pass

    def init_db(self):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS task')
        cursor.execute('DROP TABLE IF EXISTS task_log')
        cursor.execute("""create table IF NOT EXISTS task
(
	id INTEGER
		primary key autoincrement,
	filepath TEXT default '' not null,
	realpath TEXT default '' not null,
	filesize INTEGER,
	hash TEXT default '' not null,
	status INTEGER default 0 not null,
	drive_id TEXT default '' not null,
	file_id TEXT default '' not null,
	upload_id TEXT default '' not null,
	part_number INTEGER default 0 not null,
	chunk_size INTEGER default 104857600 not null,
	create_time INTEGER default 0 not null,
	finish_time INTEGER default 0 not null,
	spend_time INTEGER default 0 not null
);""")

        cursor.execute('''create table IF NOT EXISTS task_log
(
    id          INTEGER not null
        constraint task_log_pk
            primary key autoincrement,
    task_id     INTEGER,
    log_level       TEXT    default 'info' not null,
    content     TEXT    default '' not null,
    create_time INTEGER default 0 not null
);''')

    def migrate_aliyundrive(self):
        self.init_db()
        print('初始化数据库成功！')


if __name__ == "__main__":
    aliyundrive_uploader_migrate().migrate_aliyundrive()
