import socket
import time

def scan(target, maxrange=1000, maxtimeout=0.2):
    if not target:
        return None

    print(f'starting scan on: {target}')

    open_ports = {}
    timer = time.time()

    for port in range(1, maxrange+1):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket.setdefaulttimeout(maxtimeout)
        pingtime = time.time()
        result = s.connect_ex((target, port))
        if result == 0:
            connection_time = (time.time()-pingtime) * 1000
            print(f"an open port on: {port}🟢, connection took: {connection_time}ms")
            open_ports[port] = connection_time
        else:
            print(f"port {port} is closed 🔴")
        s.close()

    print(f'closing, scan took: {(time.time()-timer):.5f}s.')
    print('\nOpen ports found:')

    for values in open_ports:
        print(f'online port: {values}   || {open_ports[values]:.2f}ms 🟢')
    
if __name__ == "__main__":
    target, maxrange, maxtimeout = input('input the target address: '), int(input('input the maximum of range to scan in: ')), float(input('input the maximum timeout to range of: '))
    scan(target, maxrange, maxtimeout)