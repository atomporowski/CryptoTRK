import config
from website import create_app
from config import SECRET_KEY


app = create_app()

if __name__ == '__main__':
    app.secret_key = config.SECRET_KEY
    app.run(debug=True)
