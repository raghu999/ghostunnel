#!/usr/bin/env python3

from subprocess import Popen
from common import *
import socket, ssl, time, os, signal

if __name__ == "__main__":
  ghostunnel = None
  try:
    # create certs
    root = RootCert('root')
    root.create_signed_cert('server')

    # start ghostunnel with bad flags
    ghostunnel = run_ghostunnel(['client', '--listen={0}:13001'.format(LOCALHOST),
      '--target={0}:13002'.format(LOCALHOST), '--keystore=server.p12',
      '--connect-proxy=ftp://invalid', '--cacert=root.crt',
      '--status={0}:{1}'.format(LOCALHOST, STATUS_PORT)])

    # wait for ghostunnel to exit and make sure error code is not zero
    ret = ghostunnel.wait(timeout=20)
    if ret == 0:
      raise Exception('ghostunnel terminated with zero, though flags were invalid')  
    else:
      print_ok("OK (terminated)")
  finally:
    terminate(ghostunnel)
