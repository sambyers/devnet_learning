from intersight import Intersight
import json

api = Intersight()

r = api.ntppolicy.get()
print(json.dumps(r, indent=4))