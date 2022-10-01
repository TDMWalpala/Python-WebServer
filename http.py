import socket as soc
import os
import mimetypes as mim


HOST = "127.0.0.1" # Standard loopback interface address (localhost)
PORT = 2728  # Port to listen on (non-privileged ports are > 1023)
HTDOCS = "htdocs"


def get_res_path(http_path: str): #get resource path
    if http_path.endswith('/'):
        http_path = http_path[0:-1] 
    print(http_path, http_path.split('.'))
    path_segments = http_path.split('.')
    if not (http_path == ''):
        if len(path_segments) > 1:
            print("Requested a file with extension")
            html_file_path = os.path.join(
                os.getcwd(), HTDOCS, http_path[1:])
        else:
            html_file_path = os.path.join(
                os.getcwd(), HTDOCS, f"{http_path[1:]}.html")
    else:
        html_file_path = os.path.join(os.getcwd(), HTDOCS, "index.html")
    print(html_file_path)
    return html_file_path


server_soc = soc.socket(
    family=soc.AddressFamily.AF_INET, type=soc.SocketKind.SOCK_STREAM) # creates a socket object

server_soc.bind((HOST, PORT))  # binding host and port
server_soc.listen() # starts listening

while True:
    client_soc, client_address = server_soc.accept()
    client_raw_msg = client_soc.recv(1024)
    client_msg = client_raw_msg.decode()
    raw_http_headers = client_msg.split("\r\n")
    http_mpv_header = raw_http_headers[0]
    http_mpv_header_segments = http_mpv_header.split(" ")
    try:
        http_url = http_mpv_header_segments[1]
        http_path = http_url.split('?')[0]
        resource_path = get_res_path(http_path)
        try:
            resource = open(resource_path, "r")
            resource_content = resource.read()
            resource.close()
            content_type = mim.guess_type(resource_path)
            http_response = f"HTTP/1.1 200 OK\r\nServer: My Custom Server\r\nContent-Length: {len(resource_content)}\r\nContent-Type: {content_type[0]}\r\n\n{resource_content}"
            client_soc.sendall(http_response.encode())
        except FileNotFoundError:
            client_soc.sendall("HTTP/1.1 404 Not Found".encode())
    except IndexError:
        client_soc.sendall("HTTP/1.1 400 Bad Request".encode())

    client_soc.close()
