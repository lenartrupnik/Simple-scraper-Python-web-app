import psycopg2, json

class DatabaseConnector:
    def __init__(self):
        config = self.load_config()
        
        try:
            self.conn = psycopg2.connect(
                dbname=config['dbname'], 
                user=config['user'], 
                password=['password'], 
                host=['host'], 
                port='port')
            self.cur = self.conn.cursor()
            
            # Print PostgreSQL server version
            self.cur.execute("SELECT version();")
            record = self.cur.fetchone()
            print("You are successfully connected to - ", record, "\n")
            
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS items(
                id serial PRIMARY KEY,
                title TEXT,
                image_url TEXT
            )""")
            
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        
    def get_cursor(self):
        return self.cur
    
    def load_config(filename='config.json'):
        with open(filename) as f:
            config = json.load(f)
            
        return config