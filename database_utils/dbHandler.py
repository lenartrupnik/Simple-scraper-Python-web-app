import psycopg2, json

class DBHandler:
    """
    A class to handle connections to a PostgreSQL database.

    Attributes:
        conn (psycopg2.extensions.connection): The database connection.
        cur (psycopg2.extensions.cursor): The database cursor.
    """
    def __init__(self):
        """
        Initializes the DBHandler by establishing a connection to the PostgreSQL database.
        """
        config = self.load_config()
        try:
            self.conn = psycopg2.connect(
                dbname=config['dbname'], 
                user=config['user'], 
                password=config['password'], 
                host=config['host'], 
                port=config['port'])
            
            self.cur = self.conn.cursor()
            
            self.cur.execute("SELECT version();")
            record = self.cur.fetchone()
            print("You are successfully connected to - ", record, "\n")
            
            # Make sure a table is in the database
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS items(
                id serial PRIMARY KEY,
                title TEXT,
                image_url TEXT
            )""")
            
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        
    def get_cursor(self):
        """
        Returns:
            psycopg2.extensions.cursor: The database cursor.
        """
        return self.cur
    
    def get_conn(self):
        """
        Returns:
            psycopg2.extensions.connection: The database connection.
        """
        return self.conn
    
    def load_config(self, filename='../database_utils/config.json'):
        """
        Loads the database configuration from a JSON file.
        
        Args:
            filename (str, optional): The path to the JSON configuration file. 
            Defaults to '../database_utils/config.json'.

        Returns:
            dict: The database configuration.
        """
        with open(filename, "r") as f:
            config = json.load(f)
            
        return config
    
    def close(self):
        """
        Closes the database cursor and connection.
        """
        self.cur.close()
        self.conn.close()