from client import Client

import select

class server_state:
    def __init__(self):
        self.clients = list()
        # List of client/priority tuples.
        self.possessions = dict()

    def connect(self, client):
        if client in self.clients:
            raise ValueError("client already in list")
        self.clients.append(Client(client[0], client[1]))

    def disconnect(self, client):
        if client not in self.clients:
            raise ValueError("client not in list")
        self.clients.remove(client)
        for slave in self.possessions:
            slave_data = self.possessions[slave]
            if slave_data[0] == client:
                self.release_possession(client, slave)

    def take_possession(self, client, priority, slave):
        if client not in self.clients:
            raise ValueError("client not in list")
        if slave in self.possessions:
            slave_data = self.possessions[slave]
            if slave_data[0] != client and slave_data[1] >= priority:
                return False
        self.possessions[slave] = (client, priority)
        return True

    def release_possession(self, client, slave):
#        if client not in self.clients:
#            raise ValueError("client not in the list")
        if self.possessions[slave][0] != client:
            raise ValueError("client is not the owner of the slave.")
        self.possessions[slave] = (None, -1)

    def get_owner(self, name):
        if name not in self.possessions:
            print("No owner")
            return None
        return self.possessions[name][0]

    def get_clients(self):
        return self.clients

    def get_client_by_name(self, name):
        for client in self.clients:
            if name == client.name:
                return client
        return None

    def get_readable_clients(self, timeout):
        sockets = [client.socket for client in self.clients]
        readable, _, _ = select.select(sockets, [], [], timeout)
        return [client for client in self.clients if client.socket in readable]
