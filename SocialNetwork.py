from user import User

'''
I added an error alert that will pop up to the user in the sign_up function.
It will be written to the user what errors he made:
"There is already such a username on the network"
or
"The password is not the right length"
'''


# Creating a network, using the singleton design method
class SocialNetwork:
    __instance = None
    __is_initialized = False

    def __new__(cls, name: str):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name: str):
        if self.__is_initialized:
            return
        self.name = name
        self.users = dict()
        self.__is_initialized = True
        print(f"The social network" + " " + self.name + " " + "was created!")

    def __str__(self):
        result = f"{self.name} social network:\n"
        for user in self.users.values():
            result += str(user) + "\n"
        return result

    def sign_up(self, username, password):  # Network registration
        if username not in self.users:
            if 4 <= len(password) & len(password) <= 8:
                new_user = User(username, password, True)
                self.users[new_user.username] = new_user
                return new_user
            else:
                raise ValueError("Password length should be between 4 and 8 characters")
        else:
            raise ValueError(f"Username {username} is already in use")

    def log_out(self, username):  # Disconnecting from the network
        if username in self.users:
            self.users[username].connect = False
        print(f"{username} disconnected")

    def log_in(self, username, password):  # Connecting to the network (after registering for the network)
        if username in self.users and self.users[username].password == password:
            self.users[username].connect = True
        print(f"{username} connected")
