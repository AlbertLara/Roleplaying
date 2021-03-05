from project.application import create_full_app
import os


app = create_full_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT"),5000)
    app.run(host="0.0.0.0",port=port)