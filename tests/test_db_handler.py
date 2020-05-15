from models.database_handler import DBHandler

if __name__ == '__main__':
    db = DBHandler('../local.db')

    db.open_connection()
    db.create_alarm_table()

    result = db.select_all()

    db.close_connection()

    print(result)