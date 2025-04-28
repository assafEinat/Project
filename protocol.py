SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
COMMAND_LENGTH = 2
DATA_LENGTH = 8
SPACES_BETWEEN_PARAMS = "@@@@$$$$@@$@%!@$"


def recv_data(client_socket):
    cmd_len = int(recv_until_done(client_socket, COMMAND_LENGTH))

    command = recv_until_done(client_socket, cmd_len)

    data_len = int(recv_until_done(client_socket, DATA_LENGTH))

    data = recv_until_done(client_socket, data_len)
    
    data = seperate_params(data)

    return command, data


def recv_until_done(client_socket, wanted_len):
    data = ""
    while len(data) < wanted_len:
        data += client_socket.recv(wanted_len-len(data)).decode()
    return data




def send_msg(client_socket, command, data):
    completed_command = create_command(command)
    completed_data = create_msg(data)

    client_socket.sendall(completed_command)
    client_socket.sendall(completed_data)


def create_command(command):
    return (str(len(command)).zfill(COMMAND_LENGTH) + command).encode()


def seperate_params(data):
    params = data.split(SPACES_BETWEEN_PARAMS)
    
    params = [p for p in params if p]

    return params


def create_msg(data):
    return f"{str(len(data)).zfill(DATA_LENGTH)}{data}".encode()
