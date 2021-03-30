import os
import dbl


def dbl_init(client):
    dbl_client = dbl.DBLClient(client, os.getenv("DBL_TOKEN"), autopost=True)
    return dbl_client


