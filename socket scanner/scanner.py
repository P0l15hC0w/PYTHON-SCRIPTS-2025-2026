import socket
import time

target = input('input an url or path to the desired target: ')

maxrange = int(input('input the range to scan in: '))
if maxrange > 10000:
    maxrange = 10000

maxtimeout = float(input('input the default timeout (in seconds) (float): '))
if maxtimeout > 10:
    maxrange = 10
elif maxtimeout < 0.0005:
    maxtimeout = 0.0005

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
    print(f'online port: {values} || {open_ports[values]:.2f}ms 🟢')