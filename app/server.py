import app.controllers
from app.router import Router


class Application:
    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']

        try:
            return Router.resolve(path=path, method=method)(environ, start_response)
        except Exception as e:
            if str(e) == 'Requested path "/favicon.ico" not found':
                pass
            else:
                environ['exception'] = e
                return Router.resolve(path='/exception', method='GET')(environ, start_response)
