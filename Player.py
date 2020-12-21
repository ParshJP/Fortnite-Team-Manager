class Player:               #player object
    def __init__(self):
        self.last = ""
        self.first = ""         #vars for player info
        self.full = self.first + self.last
        self.rating = 0
        self.tier = ""

    def setLast(self, name):
        '''
        Sets the last name of the Player object

        PARAMETERS:
        -----------
        name
        Type: string
            The last name of the Player
        '''
        self.last = name

    def setFirst(self, name):
        '''
        Sets the first name of the Player object

        PARAMETERS:
        -----------
        name
        Type: string
            The first name of the Player
        '''
        self.first = name

    def setRating(self, rating):
        '''
        Sets the rating of the Player object

        PARAMETERS:
        -----------
        rating
        Type: integer
            The rating of the Player
            Error occurs if the rating is not an integer. User should check for validity
        '''
        rating = int(rating)
        self.rating = rating

    def setTier(self, tier):
        '''
        Sets the tier of the Player object

        PARAMETERS:
        -----------
        str
            The tier of the Player
        '''
        self.tier = tier

    def setFull(self, first, last):
        '''
        Sets the full name of the Player object

        PARAMETERS:
        -----------
        first
        Type: string
            The first name of the Player
        last
        Type: string
            The last name of the Player
        '''
        self.full = first + ' ' + last

    def getFull(self):
        '''
        Returns the full name of the Player object

        RETURNS:
        --------
        str
            The full name of the Player object
        '''
        return self.full

    def getLast(self):
        '''
        Returns the last name of the Player object

        RETURNS:
        --------
        str
            The last name of the Player object
        '''
        return self.last

    def getFirst(self):
        '''
        Returns the first name of the Player object

        RETURNS:
        --------
        str
            The first name of the Player object
        '''
        return self.first

    def getRating(self):
        '''
        Returns the rating of the Player object

        RETURNS:
        int
            The rating of the Player object
        '''
        return self.rating

    def getTier(self):
        '''
        Returns the tier of the Player object

        RETURNS:
        --------
        str
            The tier of the Player object
        '''
        return self.tier

