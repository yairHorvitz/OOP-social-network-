from abc import ABC, abstractmethod
from Post import PostFactory

'''
 I added a message alert in an extreme case in several functions:
 follow, unfollow, publish_post.
 "An attempt to change the network when not connected to the network"

 In the "publish_post" function, if I hadn't used the "observer" formatting method,
 I would have written the two lines marked in the comment.
 They would have already sent all my followers a notification that I posted
'''


# The first three classes use the observer design method.
# which takes care of updating a user's followers when uploading a post
class Sender(ABC):
    def __init__(self):
        self.whoFollowMe = set()  # Initialize as an empty set

    @abstractmethod
    def follow(self, user):
        pass

    @abstractmethod
    def unfollow(self, user):
        pass

    def notify(self, message):
        for member in self.whoFollowMe:
            member.update(message)


class Member(ABC):
    @abstractmethod
    def update(self, message):
        pass


class User(Sender, Member):
    def __init__(self, username, password, connect: bool = True, numberOfPost=0):
        super().__init__()
        self.username = username
        self.password = password
        self.connect = connect
        # self.whoFollowMe = set()   # Initialize as an empty set
        self.receivedPost = []  # Initialize as an empty list # username:Post/like/comment
        self.numberOfPost = numberOfPost

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {self.numberOfPost}, Number of followers: {len(self.whoFollowMe)}"

    def follow(self, user):  # A function that follows another user
        if self.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")
        user.whoFollowMe.add(self)  # added the name of the user who follows you to the list
        print(f"{self.username} started following {user.username}")

    def unfollow(self, user):  # A function that removes a follower from another user
        if self.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")
        if self in user.whoFollowMe:
            user.whoFollowMe.remove(self)  # removed the name of the user who follows you to the list
            print(f"{self.username} unfollowed {user.username}")

    # A function through which a post is generated
    def publish_post(self, post_type, content=None, cost=None, location=None):
        if self.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")
        # for i in self.whoFollowMe:
        #     i.receivedPost.append(f"{self.username} has a new post")
        self.notify(message=f"{self.username} has a new post")
        self.numberOfPost += 1
        return PostFactory.create_post(self, post_type, content, cost, location)

    def print_notifications(self):  # A function that prints all the posts a user has received
        print(f"{self.username}'s notifications:")
        for i in self.receivedPost:
            print(i)

    # A function that implements the design method. and adds a notification to each follower,
    # about creating a post from the person they follow
    def update(self, message):
        self.receivedPost.append(message)
