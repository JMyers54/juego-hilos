import mariadb as sql

class ConexionDB():
    def __init__(self):
        self.__host="localhost"
        self.__port = 3307
        self.__user="root"
        self.__password=""
        self.__database="juego_hilos"
        self.__connection = None

    def getConnection(self):
        return self.__connection

    def crearConexion(self):
        self.__connection = sql.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            port = self.__port,
            database = self.__database
        )
    
    def cerrarConexion(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None