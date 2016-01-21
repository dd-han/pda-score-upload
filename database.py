import pymysql.cursors
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_CHARSET


def makeConn():
    # Connect to the database
    connection = pymysql.connect(host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_DATABASE,
            charset=DB_CHARSET,
            cursorclass=pymysql.cursors.DictCursor)
    return connection


def getPlayer():
    result=False
    try:
        connection=makeConn()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `Player`'
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
        return result

def getSong():
    result=False
    try:
        connection=makeConn()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `Songs`'
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
        return result

def getScore(Player,Song,Start,Amount):
    result=False
    try:
        connection=makeConn()
        with connection.cursor() as cursor:
            sql = 'SELECT `ScoreDate`,`ImageHash`,`Rate` FROM `Score` \
            WHERE `PlayerID` = %s AND `SongID` = %s \
            ORDER BY `ScoreDate` DESC LIMIT %s OFFSET %s'
            cursor.execute(sql, (Player,Song,Amount,Start) )
            result = cursor.fetchall()
    finally:
        connection.close()
        return result

def lookupPlayer(FBID):
    result=False
    try:
        connection=makeConn()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `Player` WHERE `FBID` = %s'
            cursor.execute(sql,FBID)
            result = cursor.fetchone()
    finally:
        connection.close()
        return result

def insScore(Player,Song,HASH,Rate):
    result=False
    try:
        connection=makeConn()
        with connection.cursor() as cursor:
            sql = 'INSERT INTO `Score` (`PlayerID`, `SongID`, `ImageHash`, `Rate`) \
            VALUES ( %s, %s, %s, %s)'
            cursor.execute(sql, (Player,Song,HASH,Rate) )
            connection.commit()
            result=True
    finally:
        connection.close()
        return result
        
    #with connection.cursor() as cursor:
    #    # Create a new record
    #    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    #    
    #    # connection is not autocommit by default. So you must commit to save
    #    # your changes.
    #    connection.commit()

    #with connection.cursor() as cursor:
    #    # Read a single record
    #    sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    #    cursor.execute(sql, ('webmaster@python.org',))
    #    result = cursor.fetchone()
    #    print(result)

