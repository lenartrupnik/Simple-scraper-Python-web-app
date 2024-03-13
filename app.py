from flask import Flask, render_template
from database_utils.dbHandler import DBHandler
import logging

app = Flask(__name__)


@app.route('/')
def show_items():
    try:
        # Connect to PostgreSQL database
        db_handler = DBHandler()
        cur = db_handler.get_cursor()
        
        # Fetch items from database
        cur.execute("SELECT id, title, image_url FROM items")
        items = cur.fetchall()
        db_handler.close()

        # Render HTML template with fetched data
        return render_template('index.html', items=items)

    except Exception as e:
        logging.error(f'An error occurred when building app: {e}')
        return "An error occurred while processing web app"

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
