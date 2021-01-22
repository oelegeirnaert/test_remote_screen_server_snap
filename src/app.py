#!/usr/bin/python

import os, sys
import subprocess
import socket


import logging
import threading

from remotescreens import machine_info

from remotescreens.rs_print import RSPrint
from remotescreens.remotescreens import RemoteServer

log = logging.getLogger(__name__)

host = "https://remotescreens.herokuapp.com"
if socket.gethostname().lower() == "oeste":
    host = "http://localhost:8000"


def help():
    machine_info.get_all_info()


def status():
    rm = RemoteServer(host)
    rm.status()


def start():
    "Run the application"

    # rs = RSPrint()
    # rs.print_test()
    rm = RemoteServer(host)
    rm.start_server()


if __name__ == "__main__":
    status()
