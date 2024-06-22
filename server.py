import socket
import pickle
import threading

#we are defining the server configuration constants
SERVER_ADDRESS = "172.31.44.91"   #"127.0.0.1"  # replace by the corresponding router address
SERVER_PORT = 8888
BUFFER_SIZE = 4096
FILES_DIRECTORY = "files"

class FileSystem:
    def __init__(self):
        # we have initialize an empty dictionary to store file data
        self.files = {}

    def list_files(self):
        # this function returns a list of filenames
        return list(self.files.keys())

    def create_file(self, filename):
        # we check if the file already exists
        if filename not in self.files:
            # If the file does not exist, add it to the dictionary
            self.files[filename] = ""
            return True  # Return True indicates successful creation
        else:
            return False  # Return False if the file already exists

    def delete_file(self, filename):
        # we first check if the file exists
        if filename in self.files:
            # if the file exists, we will delete it from the dictionary
            del self.files[filename]
            return True  # True indicates successful deletion
        else:
            return False  # False if the file does not exist

    def rename_file(self, old_filename, new_filename):
        # we check if the old filename exists in the file system
        if old_filename in self.files:
            # we rename the file by updating the dictionary key
            self.files[new_filename] = self.files.pop(old_filename)
            return "File renamed"  # file renamed successfully message
        else:
            return "File not found"  # we return a message indicating the file was not found
    
    def clear_file(self, filename):
        # we check if the file exists
        if filename in self.files:
            # if it do exists, clear the contents of the file by setting it to an empty string
            self.files[filename] = ""
            return True  # True to indicates successful clearing
        else:
            return False  # False if the file does not exist
    
    def write_file(self, filename, data):
        # we check if the file exists
        if filename in self.files:
            # we append data to the file, removing any newline characters from the data
            if self.files[filename] == "":
                self.files[filename] += data[2:-1]
            else:
                self.files[filename] += " "
                self.files[filename] += data[2:-1]
            return True  # True to indicates successful writing
        else:
            return False  # False if the file does not exist
    
    def read_file(self, filename):
        # we check if the file exists
        if filename in self.files:
            # we check if the file is empty
            if self.files[filename] == "":
                return "File empty"  # a message indicating the file is empty
            return self.files[filename]  # we return the content of the file
        else:
            return "File not found"  


def handle_client(client_socket, file_system, client_address):
    try:
        while True:
            # it receive request from the client
            request = client_socket.recv(BUFFER_SIZE).decode()
            
            # now check if the request is empty
            if not request:
                break
            
            # it handles different types of requests
            if request.startswith("LIST"):  # Request to list files
                # we get the list of files from the file system
                files = file_system.list_files()
                # we serialize the list of files using pickle
                response = pickle.dumps(files)
                # Sending the response back to the client
                client_socket.send(response)
                
            elif request.startswith("CREATE"):  # Request to create a file
                # we're extracting the filename from the request
                _, filename = request.split(maxsplit=1)
                # we attempt to create the file in the file system
                success = file_system.create_file(filename)
                # this generates the appropriate response based on success
                response = b"File created" if success else b"File already exists"
                # we send the response back to the client
                client_socket.send(response)

            elif request.startswith("DELETE"):  # Request to delete a file
                # we're extracting the filename from the request
                _, filename = request.split(maxsplit=1)
                # it attempts to delete the file from the file system
                success = file_system.delete_file(filename)
                # we generate the appropriate response based on success
                response = b"File deleted" if success else b"File not found"
                # sending the response back to the client
                client_socket.send(response)
                
            elif request.startswith("RENAME"):  # Request to rename a file
                # we're extracting the filename from the request
                _, old_filename, new_filename = request.split(maxsplit=2)
                # this attempts to rename the file in the file system
                response = file_system.rename_file(old_filename, new_filename)
                # sending the response back to the client
                client_socket.send(response.encode())
                
            elif request.startswith("CLEAR"):  # Request to clear content of a file
                _, filename = request.split(maxsplit=1)
                # Attempt to clear the content of the file in the file system
                success = file_system.clear_file(filename)
                # generating the appropriate response based on success
                response = b"File content cleared" if success else b"File not found"
                # sending the response back to the client
                client_socket.send(response)
                
            elif request.startswith("WRITE"):  # Request to write data to a file
                _, filename, data = request.split(maxsplit=2)
                # Attempt to write data to the file in the file system
                success = file_system.write_file(filename, data)
                # generating the appropriate response based on success
                response = b"File written" if success else b"File not found"
                # sending the response back to the client
                client_socket.send(response)
                
            elif request.startswith("READ"):  # Request to read content of a file
                _, filename = request.split(maxsplit=1)
                # we are reading the content of the file from the file system
                data = file_system.read_file(filename)
                # send the content back to the client
                client_socket.send(data.encode())
                
            elif request.strip() == "EXIT":  # Handling client exit request
                break
                
            else:  # this is handling invalid requests
                client_socket.send(b"Invalid request")

    except ConnectionResetError:  # Handling unexpected disconnection errors
        print(f"Client {client_address} disconnected unexpectedly")
    
    except Exception as e:  # this is to handle other exceptions
        print("Error:", e)  # Print the error message
        client_socket.send(b"Error processing request")  # and we send that error message to the client
    
    finally:  # Performing cleanup actions
        client_socket.close()  # Closing the client socket
        print(f"Client {client_address} disconnected") 


def main():
    # Creating a new instance of the FileSystem class
    file_system = FileSystem()

    # we are creating a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # now, we bind the socket to the server address and port
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    # now the server starts listening for incoming connections with a maximum backlog of 5
    server_socket.listen(5)
    print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        # it is accepting a new connection
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")
        # we start a new thread to handle each client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, file_system, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
