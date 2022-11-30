class usuario:
    #Constructor
    def __init__(self, email, password, nick):
        #instance attributes
        self.email = email
        self.password = password
        self.nick = nick
    def __str__(self):
        return self.email + ";" + self.password + ";" + self.nick + ";"