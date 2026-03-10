"""
Includes the Config and Sys variables that would be used across files

"""


# implement container name capture in status

import socket
hostname = socket.gethostname()



# check for startup_complete state
startup_complete = False


# variable shutdown to initiate prestop hook
shutdown = False
