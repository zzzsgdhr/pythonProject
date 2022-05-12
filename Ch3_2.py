import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='scraper1',
                             password='password',
                             db='DB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('example@example.org', 'password'))

    connection.commit()

    with connection.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `email` = %s"
        cursor.execute(sql, ('example@example.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
