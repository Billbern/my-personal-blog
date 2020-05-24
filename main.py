import os
from personalblog import blog


if __name__ == "__main__":
    host = os.environ.get('IP', '127.0.1.1')
    port = int(os.environ.get('PORT', 8080))
    blog.run(host=host, port=port, debug=True, use_reloader=True)