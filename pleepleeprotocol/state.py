from client import Client

import select

class server_state:
    """Placeholder class for the server data.
    """

    def __init__(self):
        self.clients = list()
        # List of client/priority tuples.
        self.possessions = dict()

    def connect(self, client):
        """Add a client to the list of connected clients.

        Args:
            client: The new client.
        """
        if client in self.clients:
            raise ValueError("client already in list")
        self.clients.append(Client(client[0], client[1]))

    def disconnect(self, client):
        """Remove an existing client from the list of clients. Release its
        owned devices.

        Args:
            client: The disconnected client.
        """
        if client not in self.clients:
            raise ValueError("client not in list")
        self.clients.remove(client)
        for slave in self.possessions:
            slave_data = self.possessions[slave]
            if slave_data[0] == client:
                self.release_possession(client, slave)

    def take_possession(self, client, priority, slave):
        """Decides whether a client can take possession of a device and do it
        if allowed.

        Args:
            client: The client that issued the request.
            priority: The priority on the device. Used to determine if the current owner can be replaced.
            slave: The name of the device to own.

        Return:
            True if possession is taken successfully, False otherwise.
        """
        if client not in self.clients:
            raise ValueError("client not in list")
        if slave in self.possessions:
            slave_data = self.possessions[slave]
            if slave_data[0] != client and slave_data[1] >= priority:
                return False
        self.possessions[slave] = (client, priority)
        return True

    def release_possession(self, client, slave):
        """Release a device.

        Args:
            client: The client releaseing a possession. Must own the device.
            slave: The device to be released.
        """
#        if client not in self.clients:
#            raise ValueError("client not in the list")
        if self.possessions[slave][0] != client:
            raise ValueError("client is not the owner of the slave.")
        self.possessions[slave] = (None, -1)

    def get_owner(self, name):
        """Get the current owner of a device

        Args:
            name: The name of the device.

        Return:
            A string identifying the owner if the device is owned by a client, None otherwise.
        """
        if name not in self.possessions:
            print("No owner")
            return None
        return self.possessions[name][0]

    def get_clients(self):
        """Get the list of connected clients.
        """
        return self.clients

    def get_client_by_name(self, name):
        """Search a client by name.

        Args:
            name: The name of the sought client.

        Return:
            The Client instance if existing, None otherwise.
        """
        for client in self.clients:
            if name == client.name:
                return client
        return None

    def get_readable_clients(self, timeout):
        """Do a select on the clients to both sleep if nothing to read or get the
        list of clients that have sent data.

        Args:
            timeout: How much time, in seconds, to wait at most.

        Return:
            The list of client having something to receive from.
        """
        sockets = [client.socket for client in self.clients]
        readable, _, _ = select.select(sockets, [], [], timeout)
        return [client for client in self.clients if client.socket in readable]
