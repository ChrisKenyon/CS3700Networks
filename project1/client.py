import argparse
import socket
import ssl

TCP_PORT = 27993
BUFFER = 1024

def run_client(args):
    host = args.hostname
    port = args.p
    nuid = args.neu_id
    secure = args.s

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.SSLSocket(sock) if secure else sock
    sock.connect((host, port))

    message = 'cs3700fall2016 HELLO {}\n'.format(nuid)
    while True:
        sock.send(bytes(message,'utf-8'))
        response = sock.recv(BUFFER)
        response_str = response.decode('utf-8').strip()
        if "STATUS" in response_str:
            operation = response_str.split('STATUS ')[1]
            answer = int(eval(operation))
            message = "cs3700fall2016 {}\n".format(answer)
        elif "BYE" in response_str:
            secret_flag = response_str.split('BYE ')[1]
            break
        else:
            sock.close()
            raise Exception('Unexpected Response')
    sock.close()
    print(secret_flag)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=int)
    parser.add_argument("-s", action="store_true")
    parser.add_argument("hostname")
    parser.add_argument("neu_id")
    args = parser.parse_args()
    if not hasattr(args, "p"):
        args.p = TCP_PORT
    run_client(args)
