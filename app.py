from flask import Flask, render_template
import psycopg2, os

app = Flask(__name__)

@app.route('/')
def show_items():
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname='scrapy_db',
        user='postgres',
        password='1Q2W3E4r!',
        host='db'
    )
    cur = conn.cursor()
    
    cur.execute("SELECT id, title, image_url FROM items")
    items = cur.fetchall()
    print(len(items))
    
    # Close database connection
    cur.close()
    conn.close()
    
    # Render HTML template with fetched data
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=8080)