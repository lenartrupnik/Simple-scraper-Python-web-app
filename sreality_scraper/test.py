import psycopg2

def test_database_connection():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname='scrapy_db',
            user='postgres',
            password='1Q2W3E4r!',
            host='db',
            port='5432'
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a test query
        cur.execute('SELECT version()')

        # Fetch and print the result
        db_version = cur.fetchone()
        print('Connected to the PostgreSQL database. Server version:', db_version[0])
        
         # Execute the DELETE statement
        cur.execute('DELETE FROM items')

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print('Unable to connect to the PostgreSQL database:', e)

if __name__ == "__main__":
    test_database_connection()
