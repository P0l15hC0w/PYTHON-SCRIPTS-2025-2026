import socket
import time
import threading
import queue

def scan(target, maxrange=1000, maxtimeout=0.2, threads=10):
    if not target:
        return None

    print(f"starting scan on: {target}")
    print(f"threads: {threads}, timeout per thread: {maxtimeout / threads:.3f}s")

    port_queue = queue.Queue()
    open_ports = {}
    open_ports_lock = threading.Lock()

    thread_timeout = maxtimeout / threads

    for port in range(1, maxrange + 1):
        port_queue.put(port)

    timer = time.time()

    def worker():
        while not port_queue.empty():
            try:
                port = port_queue.get_nowait()
            except queue.Empty:
                return

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(thread_timeout)

            pingtime = time.time()
            result = s.connect_ex((target, port))

            if result == 0:
                connection_time = (time.time() - pingtime) * 1000
                with open_ports_lock:
                    open_ports[port] = connection_time
                print(f"an open port on: {port} 🟢, connection took: {connection_time:.2f}ms")
            else:
                print(f"port {port} is closed 🔴")

            s.close()
            port_queue.task_done()

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print(f"\nclosing, scan took: {(time.time() - timer):.5f}s.")

    if not open_ports:
        print("\nNo open ports were found.")
        return None
    else:
        print("\nOpen ports found:")
        for port in sorted(open_ports):
            print(f"online port: {port}   || {open_ports[port]:.2f}ms 🟢")
        return open_ports

if __name__ == "__main__":
    target = input("input the target address: ")
    maxrange = int(input("input the maximum range to scan: "))
    maxtimeout = float(input("input the maximum timeout: "))
    threads = int(input("input number of threads: "))

    scan(target, maxrange, maxtimeout, threads)
