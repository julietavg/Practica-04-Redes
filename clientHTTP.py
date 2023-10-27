import socket
import sys

def proccessArguments():
    # Recibe argumentos desde la línea de comandos
    host_server = sys.argv[1]
    http_method = sys.argv[2]
    url = sys.argv[3]
    user_agent_option = int(sys.argv[4])
    encoding = sys.argv[5]
    connection = sys.argv[6]

    arguments = [host_server, http_method, url, user_agent_option, encoding, connection]
    return arguments

def constructHTTPRequest(host_server, http_method, url, user_agent_option, encoding, connection):
    # Construcción de HTTP request line
    version = "HTTP/1.1"
    request_line = http_method + " " + url + " " + version + "\r\n"
    
    # Opciones de User-Agent
    user_agents = {
        1: "User-Agent: Mozilla/5.0 (Linux; Android 4.1.2; GT-S6810M Build/JZ054K) AppleWebKit/537 .36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
        2: "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0",
        3: "User-Agent: CustomClient/1.0"
    }
    
    # Construcción de HTTP header lines
    host = "Host: " + host_server
    user_agent = user_agents[user_agent_option]
    accept = "Accept: */*"
    accept_charset = "Accept-Charset: UTF-8"
    accept_encoding = "Accept-Encoding: " + encoding
    accept_language = "Accept-Language: en-US"
    connection_header = "Connection: " + connection

    header_lines = host + "\r\n" + \
                   user_agent + "\r\n" + \
                   accept + "\r\n" + \
                   accept_charset + "\r\n" + \
                   accept_encoding + "\r\n" + \
                   accept_language + "\r\n" + \
                   connection_header + "\r\n"
    
    # La petición de HTTP debe terminar con un retorno de carro y un salto de línea
    blank_line = "\r\n"
    
    # Concatenación de cada parámetro para construir la petición de HTTP
    HTTP_request = request_line + header_lines + blank_line
    
    return HTTP_request.encode()  # Convertimos a bytes para enviar a través del socket

def TCPconnection(host_server, HTTP_request):
    # Crea un socket de TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conexión del cliente al servidor dado, en el puerto 80 para HTTP
    s.connect((host_server, 80))
    # Envía la petición HTTP al servidor
    s.send(HTTP_request)
    
    # Mientras reciba información del servidor, la guardará en HTTP_response, e imprimirá en pantalla
    while True:
        HTTP_response = s.recv(1024)
        if not HTTP_response: break
        print(HTTP_response.decode())
    
    # Una vez que la recepción de información ha terminado se cierra la conexión con el servidor
    s.close()
    print("\nConexión con el servidor finalizada\n")

def display_help():
    help_message = """
    Uso: python clientHTTP.py host http_method url user_agent encoding connection
    
    host: dirección IP del servidor HTTP o nombre de dominio.
    http_method: método de HTTP (HEAD o GET).
    url: archivo o recurso solicitado al servidor web.
    user_agent: opciones numeradas del 1 al 3 para diferentes user agents.
        1: Mozilla/5.0 (Linux; Android...)
        2: Mozilla/5.0 (X11; Linux x86_64...)
        3: CustomClient/1.0
    encoding: codificación de la respuesta (gzip, deflate, identity).
    connection: forma del establecimiento de la conexión (keep-alive, close).
    """
    print(help_message)

# Si el script se ejecuta directamente (no se importa como módulo)
if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in ['-h', '--help']:
        display_help()
    else:
        arguments = proccessArguments()
        HTTP_request = constructHTTPRequest(*arguments)
        TCPconnection(arguments[0], HTTP_request)
