import zerorpc
import time

c = zerorpc.Client()
while True:
    try:
        c.connect("tcp://127.0.0.1:9000")
        print('-' * 30)

        for i in range(100):
            print(c.hello(str(i) + "RPC"))
            time.sleep(1)
    except Exception as e:
        print(e)


