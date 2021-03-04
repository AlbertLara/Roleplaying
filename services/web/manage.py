from project.application import create_full_app
import os


app = create_full_app()

if __name__ == "__main__":
    app.run(host=os.getenv('HOST'),port=os.getenv('PORT'))