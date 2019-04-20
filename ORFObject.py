# Auteur: Evander van Wolfswinkel
# Created: 22-3-2019
# Functionality: Object for storing ORF information
# Known Bugs: No known Bugs
class ORF:
    """Constructor for creating ORF objects"""
    def __init__(self, sequence, length, strand, frame, header):
        self.__sequence = sequence
        self.__length = length
        self.__strand = strand
        self.__frame = frame
        self.__header = header


""" Getters and setters for storing ORF related information"""
    def get_sequence(self):
        return self.__sequence

    def set_sequence(self, sequence):
        self.__sequence = sequence

    def get_length(self):
        return self.__length

    def set_length(self, length):
        self.__length = length

    def get_strand(self):
        return self.__strand

    def set_strand(self, strand):
        self.__strand = strand

    def get_frame(self):
        return self.__frame

    def set_frame(self, frame):
        self.__frame = frame

    def get_header(self):
        return self.__header

    def set_header(self, header):
        self.__header = header
