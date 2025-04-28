import socket
from protocol import SERVER_HOST, SERVER_PORT, SPACES_BETWEEN_PARAMS, send_msg, recv_data
import os



def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")
    return client_socket


def get_code_from_file():
    file_path = input("enter the file path: ")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    print("file path does not exist")


def get_file():
    file_path = input("enter the file path: ")
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return file.read()
    print("file path does not exist")


def client_write_code():
    print("code must be in a function.")
    print("code must include white spaces every white space is 4 space buttons or 1 tab press")
    print("you can either write it all at once or one line at a time")
    print("code must end with a return")
    full_code = ""
    line = input("you are in code writing mode you can write exit to stop writing.\n")
    while line != "exit":
        full_code += line + "\n"
        line = input("")
    return full_code


def send_request(client_socket, command):
    if command == "update":
        preference_question = input("type f to get code from file,type anything else to write it: ")
        if preference_question == "f":
            function_code = get_code_from_file()
            if function_code is None:
                return
        else:
            function_code = client_write_code()
        request_data = function_code

    elif command == "add_file":
        path = input("\nwrite for the server a path with file name and type: ")
        if path == "":
            return
        request_data = get_file()
        if request_data is None:
            return
        request_data = f"{path}{SPACES_BETWEEN_PARAMS}{request_data}"
    else:
        request_data = " "
        while True:
            request = input("\nEnter data if needed if not type exit: ")
            if request == "exit":
                break
            if isinstance(request, bytes):
                request = request.decode()
            request_data += f"{SPACES_BETWEEN_PARAMS}{request}"
    send_msg(client_socket, command, request_data)

    return "cleared for receiving and continuing to work"


def receive_response(client_socket):
    response = recv_data(client_socket)[1][0]
    return response


def handle_server_response(response):
    try:
        print(f"Server response: \n{response}")
    except UnicodeDecodeError:
        print(binary_data_to_file(response))


def binary_data_to_file(file_data):
    file_name = input("enter the name you want to save the file as: ")
    file_path = input("enter the path of which you want to put the file in: ")
    if file_path == "":
        file_path = os.getcwd()  # gets current file path
    try:
        with open(fr"{file_path}\{file_name}", "wb") as new_file:
            new_file.write(file_data)
            return "file added successfully"
    except Exception as e:
        return f"couldn't add file: {e}"


def main():
    client_socket = connect_to_server()
    print("write help if you dont know what function exist")
    try:
        command_name = input("\nEnter command (or 'exit' to quit): ")
        while command_name != "exit":
            if send_request(client_socket, command_name) is not None:
                response = receive_response(client_socket)
                handle_server_response(response)
            command_name = input("\nEnter command (or 'exit' to quit): ")

    finally:
        print("Closing connection.")
        send_msg(client_socket, "exit", "exit")
        client_socket.close()


if __name__ == "__main__":
    main()
