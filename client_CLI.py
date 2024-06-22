import socket
import pickle

SERVER_ADDRESS = "172.31.44.91"   #"127.0.0.1" # replace by the corresponding router address
SERVER_PORT = 8888
BUFFER_SIZE = 4096

def send_request(server_socket, request):
    # we are sending the request to the server
    server_socket.send(request.encode())
    # we receive the response from the server
    response = server_socket.recv(BUFFER_SIZE)
    return response

def list_files(server_socket):
    # Sending a request to list files to the server
    response = send_request(server_socket, "LIST")
    # we Unpickle the response to get the list of files
    files = pickle.loads(response)
    print("Files available on server:")
    # it will print the list of files
    for filename in files:
        print(filename)

def create_file(server_socket, filename):
    # Sending a request to create a file to the server
    response = send_request(server_socket, f"CREATE {filename}")
    # we are printing the response from the server
    print(response.decode())

def delete_file(server_socket, filename):
    # Sending a request to delete a file to the server
    response = send_request(server_socket, f"DELETE {filename}")
    # Printing the response from the server
    print(response.decode())
def clear_file(server_socket, filename):
    # we are0 Constructing a request to clear the content of the specified file
    request = f"CLEAR {filename}"
    # Sending the request to the server and receive the response
    response = send_request(server_socket, request)
    # we print the response received from the server
    print(response.decode())

def rename_file(server_socket, old_filename, new_filename):
    # Constructing a request to rename the specified file
    request = f"RENAME {old_filename} {new_filename}"
    # Sending the request to the server and receive the response
    response = send_request(server_socket, request)
    # we print the response received from the server
    print(response.decode())

def write_file(server_socket, filename, data):
    # we are encoding the data as bytes
    encoded_data = data.encode()
    # Constructing a request to write the data to the specified file
    request = f"WRITE {filename} {encoded_data}"
    # Sending the request to the server and receive the response
    response = send_request(server_socket, request)
    # we print the response received from the server
    print(response.decode())

def read_file(server_socket, filename):
    # Constructing a request to read the content of the specified file
    request = f"READ {filename}"
    # Sending the request to the server and receive the response
    response = send_request(server_socket, request)
    # we print the content received from the server
    print("File content:")
    print(response.decode())

def main():
    # we are connecting to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_ADDRESS, SERVER_PORT))
    print("Connected to server")


    while True:
    # displaying menu options to the user
        print("\nOptions:")
        print("1. List files on server")
        print("2. Create file on server")
        print("3. Delete file on server")
        print("4. Rename file")
        print("5. Write data to file on server")
        print("6. Clear file content in file on server")
        print("7. Read file from server")
        print("8. Exit")
    # we prompt the user to enter their choice as he wants to perform the operation
        choice = input("Enter your choice: ")

        if choice == "1":  # it means user chooses to list files on the server
           list_files(server_socket)
        elif choice == "2":  # it means user chooses to create a file on the server
            filename = input("Enter filename to create: ")
            create_file(server_socket, filename)
        elif choice == "3":  # it means user chooses to delete a file on the server
            filename = input("Enter filename to delete: ")
            delete_file(server_socket, filename)
        elif choice == "4":  # it means user chooses to rename a file
            old_filename = input("Enter old filename: ")
            new_filename = input("Enter new filename: ")
            rename_file(server_socket, old_filename, new_filename)
        elif choice == "5":  # it means user chooses to write data to a file on the server
            filename = input("Enter filename to write to: ")
            data = input("Enter data to write: ")
            write_file(server_socket, filename, data)
        elif choice == "6":  # it means user chooses to clear content of a file on the server
            filename = input("Enter filename to clear content: ")
            clear_file(server_socket, filename)
        elif choice == "7":  # it means user chooses to read a file from the server
            filename = input("Enter filename to read: ")
            read_file(server_socket, filename)
        elif choice == "8":  # User chooses to exit
        # Sending an exit request to the server
            send_request(server_socket, "EXIT")
            break
        else:
           print("Invalid choice")  # we inform the user of an invalid choice

# we close the connection with the server
    server_socket.close()

if __name__ == "__main__":
    main()
