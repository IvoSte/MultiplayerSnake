from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

PORT_NUMBER = 5555

class EchoUDP(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        print(f"received {datagram} from {address}")
        self.transport.write(datagram, address)


def setup_server():
    print("starting server")
    reactor.listenUDP(PORT_NUMBER, EchoUDP())
    print("running server")
    reactor.run()


if __name__=="__main__":
    setup_server()