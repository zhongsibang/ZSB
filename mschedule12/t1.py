import zerorpc

class HelloRPC(object):
    def hello(self, name):
        #return "Hello, %s" % name
        pass

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:9000")
s.run()








