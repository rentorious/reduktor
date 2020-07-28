import os
from . import create_app

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app = create_app()
    app.run(host='0.0.0.0', port=port)

