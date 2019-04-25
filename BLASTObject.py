# Auteur: Evander van Wolfswinkel, Jung Ho Loos
# Created: 2-3-2019
# Functionality: Used for storing Blast information
# Known Bugs: No known Bugs

class blast:
    """Class object that stores blast information"""
    def __init__(self, sequenceName, length, Evalue):
        self.__sequenceName = sequenceName
        self.__length = length
        self.__Evalue = Evalue

    def get_sequenceName(self):
        return self.__sequenceName

    def set_sequenceName(self, sequenceName):
        self.__sequenceName = sequenceName

    def get_length(self):
        return self.__length

    def set_length(self, length):
        self.__length = length

    def get_Evalue(self):
        return self.__Evalue

    def set_Evalue(self, Evalue):
        self.__Evalue = Evalue
