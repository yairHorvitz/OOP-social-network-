from abc import abstractmethod, ABC
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

'''
 I added a message alert in an extreme case in several functions:
 like, comment, sold, discount.
 "An attempt to change the network when not connected to the network"
'''


class Post:
    def __init__(self, user):
        self.user = user

    @abstractmethod
    def like(self, user):  # A function that likes another user's post
        if user.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")
        if self.user != user:
            print(f"notification to {self.user.username}: {user.username} liked your post")
            self.user.receivedPost.append(f"{user.username} liked your post")

    @abstractmethod
    def comment(self, user, contentOfComment):  # A function that makes a comment to another user's post
        if user.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")

        print(f"notification to {self.user.username}: {user.username} commented on your post: {contentOfComment}")
        self.user.receivedPost.append(f"{user.username} commented on your post")


# This is a class, which classifies the type of post the user enters and creates it
class PostFactory:
    @staticmethod
    def create_post(user, post_type, content, cost, location):
        if post_type == "Text":
            return TextPost(user, content)
        elif post_type == "Image":
            return ImagePost(user, content)
        elif post_type == "Sale":
            return SalePost(user, content, cost, location)


class ImagePost(Post, ABC):  # A class that builds a post of type image
    def __init__(self, user, imageFile):
        super().__init__(user)
        self.imageFile = imageFile

        print(self.__str__())

    # A function that allows you to display an image. In the event of an error,
    # raise will pop up to the user about a problem with the image
    def display(self):
        try:
            image = mpimg.imread(self.imageFile)
            plt.imshow(image)
            plt.show()
            print("Shows picture")
        except Exception as e:
            raise FileNotFoundError("Error loading or displaying the image:", e)

    def __str__(self):
        return f"{self.user.username} posted a picture\n"


class SalePost(Post, ABC):  # A department that deals with the production of a sales post
    def __init__(self, user, product, cost, location):
        super().__init__(user)
        self.sale = "For sale!"
        self.product = product
        self.cost = cost
        self.location = location

        print(self.__str__())

    def __str__(self):
        return f"{self.user.username} posted a product for sale:\n{self.sale} {self.product}, price: {self.cost}, pickup from: {self.location}\n"

    # A function through which the post uploader enters a discount on the product
    def discount(self, priceOfDiscount, password):
        if self.user.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")
        if password == self.user.password:
            self.cost *= ((100 - priceOfDiscount) / 100)
            print(f"Discount on {self.user.username} product! the new price is: {self.cost}")

    # A function through which the post uploader enters a sold status on the product
    def sold(self, password):
        if self.user.connect is False:
            raise ConnectionError("You are not connected to the network, so you will not be able to make changes")
        if password == self.user.password:
            print(f"{self.user.username}'s product is sold")
            self.sale = "Sold!"


class TextPost(Post, ABC):  # A class that deals with a message type post
    def __init__(self, user, contentOfText):
        super().__init__(user)
        self.contentOfText = contentOfText

        print(self.__str__())

    def __str__(self):
        return f"{self.user.username} published a post:\n\"{self.contentOfText}\"\n"
