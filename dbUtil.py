#!flask/bin/python
# -*- coding: utf-8 -*-
from app import db, models
import time, json

def insert_new_msg( data ):
    """

    @rtype : str
    """
    statusMsg = ""
    if not ( data is None ):
        try:
            item = models.Todos(message=data[0]['message'], latitude=data[0]['latitude'], longitude=data[0]['longitude'])
            db.session.add(item)
            db.session.commit()

            statusMsg = "OK"

        except Exception, e:
            raise e

        finally:
            db.session.rollback()

    else:
        statusMsg = "ERROR"

    return dict(status=statusMsg)

