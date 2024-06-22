*****FileNest: Collaborative File Management System*****
FileNest is a collaborative file management system that allows users to perform various file operations such as creating, deleting, renaming, writing, reading, and listing files. It provides both a command-line interface (CLI) and a graphical user interface (GUI) for interacting with the file system.

*****Features*****
CLI Interface: Allows users to interact with the file system using command-line commands.
GUI Interface: Provides a user-friendly graphical interface for file management operations.
Multi-User Support: Supports multiple users accessing the file system concurrently.
File Operations: Users can create, delete, rename, write, read, and list files.
Error Handling: Includes error handling mechanisms to handle unexpected situations gracefully.

*****Python Libraries*****
socket
pickle
threading
tkinter

*****Prerequisites*****
Python: latest version of python is installed
Libraries: all the necessary libraries are installed (pip install <library>)


*****Files*****
server.py: main server
client_CLI.py: Command-line Interface client
client_GUI.py: Graphical-user Interface client

*****Usage*****
**Command-Line Interface (CLI)**
Start the server:
python server.py

Run the client:
python client.py

Follow the prompts to perform file management operations.

**Graphical User Interface (GUI)**
Start the server:
python server.py

Run the GUI client:
python client_GUI.py

Use the GUI interface to perform file management operations.

*****Configuration*****
Server Address: Modify the SERVER_ADDRESS variable in client.py and client_GUI.py to match the IP address of the server.
Server Port: Modify the SERVER_PORT variable in server.py, client.py, and client_GUI.py to specify the port number for communication.
Buffer Size: Adjust the BUFFER_SIZE variable in server.py, client.py, and client_GUI.py to configure the buffer size for data transmission.
Listen(5): Server can handle 5 clients at a time using threading on handle client function.

*****Team Members*****
B22AI051: Arjun Bhattad
B22AI056: Chirag Kumar
