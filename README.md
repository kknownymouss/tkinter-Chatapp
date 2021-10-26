# tkinter-Chatapp
A chatapp made with python's tkinter and socket modules.

# Guide
## client_side.py
You can find these constants at the top of the `client_side.py` file. Edit their values so the script can connect to the server running on `server_side.py`.
### Example:
```python
# DECLARING CONSTANTS
PORT = 11921 # Here goes the port you want to connect to
SERVER = "2.tcp.ngrok.io" # Here goes the ip address/tcp connection you want to connect to
```
## server_side.py
You can find these constants at the top of the `server_side.py` file. Edit their values so `client_side.py` can connect to the server running on this script.
### Example :
To run the server on your local machine. Use either `"0.0.0.0"` or `"127.0.0.1"` depending on your system
```python
# DECLARING CONSTANTS
PORT = 5050 # Here goes the port you want the people to connect to
SERVER = "0.0.0.0" # Here goes the ip address you want the server to run on
```
