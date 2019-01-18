import json
from tornado import web
from jupyterhub.apihandlers import  APIHandler, default_handlers

class BatchSpawnerAPIHandler(APIHandler):
    @web.authenticated
    def post(self):
        """POST set user's spawner port number"""
        user = self.get_current_user()
        data = self.get_json_body()
        port = int(data.get('port', 0))
        message = ''
        spawner = user.spawner
        try:
            from wrapspawner import WrapSpawner
            if isinstance(spawner, WrapSpawner):
                message = "WrapSpawner detected: using user.spawner.child_spawner; "
                spawner = spawner.child_spawner
        except:
            pass
        spawner.current_port = port
        message = message + "BatchSpawner port configured"
        self.finish(json.dumps({"message": message}))
        self.set_status(201)

default_handlers.append((r"/api/batchspawner", BatchSpawnerAPIHandler))
