from app import create_app
import cache

if __name__ == '__main__':
    app = create_app()
    cache.create()

    app.run(debug=True)