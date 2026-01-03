from flask import Flask
from database import db
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    USUARIO = os.getenv("DB_USER")
    SENHA = quote_plus(os.getenv("DB_PASSWORD"))
    HOST = os.getenv("DB_HOST")
    PORTA = os.getenv("DB_PORT")
    BANCO = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    from models import USUARIOS, TAREFAS
    from routes import init_routes
    init_routes(app)
    
    with app.app_context():
        db.create_all()
        
    return app

app = create_app()
if __name__ == "__main__":
    app.run()

