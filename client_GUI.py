import socket
import pickle
import tkinter as tk
from tkinter import messagebox

# we are defining server configuration constants
SERVER_ADDRESS = "172.31.44.91"     #"127.0.0.1"  # replace by the corresponding router address
SERVER_PORT = 8888
BUFFER_SIZE = 4096

def send_request(server_socket, request):
    # Sending request to server
    server_socket.send(request.encode())
    # we receive response from server
    response = server_socket.recv(BUFFER_SIZE)
    return response

def list_files(server_socket):
    # Sending a request to the server to list files
    response = send_request(server_socket, "LIST")
    # now we unpickle the response to get the list of files
    files = pickle.loads(response)
    return files

def create_file(server_socket, filename):
    # we are sending a request to the server to create a file
    response = send_request(server_socket, f"CREATE {filename}")
    return response.decode()

def delete_file(server_socket, filename):
    # we are sending a request to the server to delete a file
    response = send_request(server_socket, f"DELETE {filename}")
    return response.decode()

def clear_file(server_socket, filename):
    # we are sending a request to the server to clear the content of a file
    request = f"CLEAR {filename}"
    response = send_request(server_socket, request)
    return response.decode()
def rename_file(server_socket, old_filename, new_filename):
    # we constructing a request to rename the specified file
    request = f"RENAME {old_filename} {new_filename}"
    # we are sending  the request to the server and receive the response
    response = send_request(server_socket, request)
    # Decoding the response and return it
    return response.decode()

def write_file(server_socket, filename, data):
    # Encoding the data as bytes
    encoded_data = data.encode()
    # Constructing a request to write data to the specified file
    request = f"WRITE {filename} {encoded_data}"
    # Sending the request to the server and receive the response
    response = send_request(server_socket, request)
    # we are ecoding the response and return it
    return response.decode()

def read_file(server_socket, filename):
    # we are sending a request to read the content of the specified file
    response = send_request(server_socket, f"READ {filename}")
    # Decoding the response and return it
    return response.decode()

def list_files_command():
    try:
        # it attempt to get the list of files from the server
        files = list_files(server_socket)
        # Clearing the current contents of the files listbox
        files_listbox.delete(0, tk.END)
        # Inserting each filename from the server response into the listbox
        for filename in files:
            files_listbox.insert(tk.END, filename)
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")

def create_file_command():
    try:
        # Getting the filename from the filename entry widget
        filename = filename_entry.get()
        # Attempting to create the file on the server
        response = create_file(server_socket, filename)
        # we are updating the result label with the server response
        result_label.config(text=response)
        # Clearing the filename entry widget
        clear_file_entries()
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")

def delete_file_command():
    try:
        #we get the filename from the filename entry widget
        filename = filename_entry.get()
        #it attempt to delete the file on the server
        response = delete_file(server_socket, filename)
        # Update the result label with the server response
        result_label.config(text=response)
        # Clear the filename entry widget
        clear_file_entries()
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")
def clear_file_command():
    try:
        # Get the filename from the filename entry widget
        filename = filename_entry.get()
        # Attempt to clear the content of the file on the server
        response = clear_file(server_socket, filename)
        # Update the result label with the server response
        result_label.config(text=response)
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")

def rename_file_command():
    try:
        # Get the old and new filenames from the respective entry widgets
        old_filename = old_filename_entry.get()
        new_filename = new_filename_entry.get()
        # Attempt to rename the file on the server
        response = rename_file(server_socket, old_filename, new_filename)
        # Update the result label with the server response
        result_label.config(text=response)
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")

def write_file_command():
    try:
        # Get the filename and data from the respective entry widgets
        filename = write_filename_entry.get()
        data = write_data_entry.get()
        # Attempt to write data to the file on the server
        response = write_file(server_socket, filename, data)
        # Update the result label with the server response
        result_label.config(text=response)
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")

def read_file_command():
    try:
        # Get the filename from the filename entry widget
        filename = read_filename_entry.get()
        # Attempt to read the content of the file from the server
        content = read_file(server_socket, filename)
        # Clear the current contents of the read textbox
        read_textbox.delete(1.0, tk.END)
        # Insert the content of the file into the read textbox
        read_textbox.insert(tk.END, content)
    except:
        # If an error occurs, show an error message
        messagebox.showerror("Error", "Server is not working")

def exit_command():
    # Send an exit request to the server
    send_request(server_socket, "EXIT")
    # Quit the tkinter application
    root.quit()

def clear_file_entries():
    # Clear the contents of all filename entry widgets
    filename_entry.delete(0, tk.END)
    old_filename_entry.delete(0, tk.END)
    new_filename_entry.delete(0, tk.END)
    write_filename_entry.delete(0, tk.END)
    write_data_entry.delete(0, tk.END)
    read_filename_entry.delete(0, tk.END)
try:
    # Attempt to create a client socket and connect to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_ADDRESS, SERVER_PORT))
except:
    # If an error occurs (e.g., cannot connect to the server), show an error message
    messagebox.showerror("Error", "Cannot connect to the server")

# we're creating the main tkinter window
root = tk.Tk()
root.title("File Management Client")
root.geometry("1400x500")  # Set initial window size

# List Files
# we're creating a frame for listing files
files_frame = tk.LabelFrame(root, text="List Files", padx=10, pady=10)
files_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# we're creating a listbox to display files
files_listbox = tk.Listbox(files_frame, width=30, height=10)
files_listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# we're creating a vertical scrollbar for the listbox
scrollbar = tk.Scrollbar(files_frame, orient="vertical", command=files_listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Configuring the listbox to use the scrollbar
files_listbox.config(yscrollcommand=scrollbar.set)

# we're creating a button to refresh the file list
list_button = tk.Button(files_frame, text="Refresh List", command=list_files_command)
list_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# now we deinfe file Actions
# Frame for file actions (create, delete, clear)
actions_frame = tk.LabelFrame(root, text="File Actions", padx=10, pady=10)
actions_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Filename entry and label
filename_label = tk.Label(actions_frame, text="Filename:")
filename_label.grid(row=0, column=0, padx=5, pady=5)
filename_entry = tk.Entry(actions_frame)
filename_entry.grid(row=0, column=1, padx=5, pady=5)

# Buttons for file actions (create, delete, clear)
create_button = tk.Button(actions_frame, text="Create File", command=create_file_command)
create_button.grid(row=1, column=0, padx=5, pady=5)

delete_button = tk.Button(actions_frame, text="Delete File", command=delete_file_command)
delete_button.grid(row=1, column=1, padx=5, pady=5)

clear_button = tk.Button(actions_frame, text="Clear File Content", command=clear_file_command)
clear_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# this is to renaming the Files
# Frame for renaming files
rename_frame = tk.LabelFrame(root, text="Rename Files", padx=10, pady=10)
rename_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Old filename entry and label
old_filename_label = tk.Label(rename_frame, text="Old Filename:")
old_filename_label.grid(row=0, column=0, padx=5, pady=5)
old_filename_entry = tk.Entry(rename_frame)
old_filename_entry.grid(row=0, column=1, padx=5, pady=5)

# New filename entry and label
new_filename_label = tk.Label(rename_frame, text="New Filename:")
new_filename_label.grid(row=1, column=0, padx=5, pady=5)
new_filename_entry = tk.Entry(rename_frame)
new_filename_entry.grid(row=1, column=1, padx=5, pady=5)

# Button for renaming files
rename_button = tk.Button(rename_frame, text="Rename File", command=rename_file_command)
rename_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Write/Read Files
# Frame for writing/reading files
write_read_frame = tk.LabelFrame(root, text="Write/Read Files", padx=10, pady=10)
write_read_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

# Filename entry and label for writing
write_filename_label = tk.Label(write_read_frame, text="Filename:")
write_filename_label.grid(row=0, column=0, padx=5, pady=5)
write_filename_entry = tk.Entry(write_read_frame)
write_filename_entry.grid(row=0, column=1, padx=5, pady=5)

# Data entry and label for writing
write_data_label = tk.Label(write_read_frame, text="Data:")
write_data_label.grid(row=1, column=0, padx=5, pady=5)
write_data_entry = tk.Entry(write_read_frame)
write_data_entry.grid(row=1, column=1, padx=5, pady=5)

# Button for writing files
write_button = tk.Button(write_read_frame, text="Write File", command=write_file_command)
write_button.grid(row=2, column=0, padx=5, pady=5)

# Filename entry and label for reading
read_filename_label = tk.Label(write_read_frame, text="Filename:")
read_filename_label.grid(row=3, column=0, padx=5, pady=5)
read_filename_entry = tk.Entry(write_read_frame)
read_filename_entry.grid(row=3, column=1, padx=5, pady=5)

# Button for reading files
read_button = tk.Button(write_read_frame, text="Read File", command=read_file_command)
read_button.grid(row=4, column=0, padx=5, pady=5)

# Read File Content
# Frame for reading file content
read_frame = tk.LabelFrame(root, text="Read File Content", padx=10, pady=10)
read_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

# Textbox for displaying file content
read_textbox = tk.Text(read_frame, width=30, height=15)
read_textbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Scrollbar for the textbox
scrollbar = tk.Scrollbar(read_frame, orient="vertical", command=read_textbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Configure the textbox to use the scrollbar
read_textbox.config(yscrollcommand=scrollbar.set)

# Result Label
# Label for displaying operation results
result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

# Exit Button
# Button to exit the application
exit_button = tk.Button(root, text="Exit", command=exit_command)
exit_button.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

# Configure grid weights to make the layout expandable
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Start the tkinter main loop
root.mainloop()
