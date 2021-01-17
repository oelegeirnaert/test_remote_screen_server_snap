#!/usr/bin/python

import os, sys
import subprocess

import logging
import threading

log = logging.getLogger(__name__)


def stup():
    print("mystup!")


def main():
    from remotescreens.rs_print import RSPrint
    from remotescreens.remotescreens import RemoteServer

    from remotescreens import machine_info

    "Run the application"

    print("hello! this is a snap.")

    rs = RSPrint()
    rs.print_test()
    machine_info.get_all_info()
    rm = RemoteServer("https://remotescreens.herokuapp.com")


if __name__ == "__main__":
    main()
