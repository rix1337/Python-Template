# -*- coding: utf-8 -*-
# Python-Template
# Project by https://github.com/rix1337

import argparse
import multiprocessing
import os
import sys
import time
from socketserver import ThreadingMixIn
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

from bottle import Bottle

from rix_template.providers import shared_state, version


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass


class Server:
    def __init__(self, wsgi_app, listen='127.0.0.1', port=8080):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(self.listen, self.port, self.wsgi_app,
                                  ThreadingWSGIServer, handler_class=NoLoggingWSGIRequestHandler)

    def serve_forever(self):
        self.server.serve_forever()


def background_job(shared_state_dict, shared_state_lock):
    shared_state.set_state(shared_state_dict, shared_state_lock)
    sleep_time = 60

    try:
        while True:
            print("[Python-Template] Running job...")

            print(f"[Python-Template] Writing Example to {shared_state.values['config']} in a background thread...")
            with open(os.path.join(shared_state.values["config"], "example.txt"), "w") as f:
                f.write(shared_state.values["example"])

            print(f"[Python-Template] Job done. Sleeping for {sleep_time} seconds...")
            shared_state.update("ready", True)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        sys.exit(0)


def main():
    with multiprocessing.Manager() as manager:
        shared_state_dict = manager.dict()
        shared_state_lock = manager.Lock()
        shared_state.set_state(shared_state_dict, shared_state_lock)

        print("[Python-Template] Version " + version.get_version() + " by rix1337")
        shared_state.update("ready", False)

        parser = argparse.ArgumentParser()
        parser.add_argument("--port", help="Desired Port, defaults to 8080")
        parser.add_argument("--config", help="Desired Config Directory, defaults to ./config")
        parser.add_argument("--example", help="Example Argument")
        arguments = parser.parse_args()

        if arguments.port:
            try:
                shared_state.update("port", int(arguments.port))
            except ValueError:
                print("[Python-Template] Port must be an integer")
                sys.exit(1)
        else:
            shared_state.update("port", 8080)

        if arguments.config:
            shared_state.update("config", arguments.cache)
        else:
            shared_state.update("config", "./config")

        try:
            os.makedirs(shared_state.values["config"], exist_ok=True)
            print("[Python-Template] Config directory: " + shared_state.values["config"])
        except Exception as e:
            print("[Python-Template] Error creating config directory: " + str(e))
            sys.exit(1)

        if arguments.example:
            shared_state.update("example", arguments.example)
            print("[Python-Template] Example: " + str(shared_state.values["example"]))
        else:
            shared_state.update("example", "Default Example")
            print("[Python-Template] Example not set, using default: " + shared_state.values["example"])

        app = Bottle()

        @app.get("/")
        def status():
            return f"Python-Template v{version.get_version()} by rix1337"

        background_thread = multiprocessing.Process(target=background_job, args=(shared_state_dict, shared_state_lock,))
        background_thread.start()

        while not shared_state.values["ready"]:
            time.sleep(1)

        print(f"[Python-Template] Running at http://127.0.0.1:{shared_state.values['port']}")
        try:
            Server(app, listen='0.0.0.0', port=shared_state.values["port"]).serve_forever()
        except KeyboardInterrupt:
            background_thread.terminate()
            sys.exit(0)


if __name__ == "__main__":
    main()
