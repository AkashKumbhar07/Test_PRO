from src.app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('PORT', '8000'))
    app.run(host='0.0.0.0', port=port, debug=True)
