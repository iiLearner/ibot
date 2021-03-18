import os
import dbl
from main.main import client
dbl_client = dbl.DBLClient(client, os.getenv("DBL_TOKEN"), autopost=True)
