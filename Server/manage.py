#!/usr/bin/env python3

import datetime

from configobj import ConfigObj
from validate import Validator
from flask_script import Manager
import logging

from BetAPI import app, init_webapp
from BetAPI.model import db
from BetAPI.worker import BackgroundWorker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

manager = Manager(app)

@manager.command
def start_background_worker():
    worker = BackgroundWorker(interval=1)
    log.info('Starting worker. Hit CTRL-C to exit!')
    worker.start()
    while worker.is_alive():
        try:
            worker.join(1)
        except KeyboardInterrupt:
            log.info('Shutting down worker thread!')
            worker.stop()

@manager.command
def prime_database():
    init_webapp()
    db.session.commit()

@manager.command
def runserver(*args, **kwargs):
    app = init_webapp()
    config = ConfigObj('config/sample.config', configspec='config/sample.configspec')
    app.config_obj = config
    app.run(host='0.0.0.0', port=80,*args, **kwargs)

if __name__ == "__main__":
    manager.run()
