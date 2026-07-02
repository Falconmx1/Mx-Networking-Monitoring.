from flask import Flask
from modules.web import web_bp
import webbrowser
import threading

app = Flask(__name__)
app.register_blueprint(web_bp)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Abre el navegador automáticamente después de 1 segundo
    threading.Timer(1, open_browser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
