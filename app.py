from flask import Flask, render_template
from database_utils.dbHandler import DBHandler

app = Flask(__name__)

@app.route('/')
def show_items():
    # Connect to PostgreSQL database
    
    db_handler = DBHandler()
    cur = db_handler.get_cursor()
    cur.execute("SELECT id, title, image_url FROM items")
    items = cur.fetchall()
    db_handler.close()
    
    # Render HTML template with fetched data
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=8080)