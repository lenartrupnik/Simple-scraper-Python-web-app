import psycopg2, json

class DBHandler:
    def __init__(self):
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
    
    def get_conn(self):
        return self.conn
    
    def load_config(self, filename='../database_utils/config.json'):
        with open(filename, "r") as f:
            config = json.load(f)
            
        return config
    
    def close(self):
        self.cur.close()
        self.conn.close()