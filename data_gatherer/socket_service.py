import os
import socket
import sys
from tasks import celery

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (os.getenv('TCP_HOST', 'localhost'), int(os.getenv('TCP_PORT', 10003)))
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)


while True:
    print(sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        one_body_str = ""
        while True:
            if data := connection.recv(32):
                encoded = data.decode()
                if "<->" in encoded:
                    one_body_str += encoded.replace("<->", "")
                elif "<+>" in encoded:
                    one_body_str += encoded.replace("<+>", "")
                    celery.send_task('tasks.location', args=[], kwargs={"data": one_body_str})
                    one_body_str = ""
                else:
                    one_body_str += encoded
                connection.sendall(data)
            else:
                break
    except Exception as e:
        print(e)
    finally:
        connection.close()
