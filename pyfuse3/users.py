import os

class User():

    def __init__(self):
        self._username = os.getlogin()
        self._filename = 'root/etc/' + self._username

        try:
            file = open(self._filename, 'r')
            self._contact = file.read()
            file.close()
        except FileNotFoundError:
            print("Please enter contact information (email or phone number)")
            info = input("-->")
            self._contact = info
            file = open(self._filename, 'w+')
            file.write(self._contact)
            file.close()