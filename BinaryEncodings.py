# BinaryEncodings.py
# Below are some Binary encodings for various client/server interactions
import re

class BinaryEncodings:
    """
    returns True or False based on whether or not data is one of the binary encodings.
    """
    def __init__(self):
        self.DISCONNECT = bytes("DIS", "utf-8")
        self.CONNECT    = bytes("CON", "utf-8")
        self.MESSAGE    = bytes("MSG", "utf-8")
        self.MAP        = bytes("MAP", "utf-8")
        self._encodings = dict(self.__dict__)

    def parse(self, binary):
        """
        Decodes a binary string.
        Returns a tuple list of data types and the data they contain.
        """
        string = binary.decode()
        regexFormatStr = "("
        for v in self._encodings.values():
            regexFormatStr += re.escape(v.decode()) + "|"
        regexFormatStr = regexFormatStr[:-1] + ")"
        vector = re.split(regexFormatStr, string)
        vector.pop(0)

        packets = []
        for i in range(0,len(vector),2):
            packets.append((vector[i], vector[i+1]))

        return packets

    def unpack(self, data):
        """
        Emulates the old action of unpacking.
        This uses the above parsing tool, but only returns the first tuple.
        Why?
        Well.. The client can attempt to hack the server through use of the BinaryEncodings module.
        This prevents that.
        """
        return self.parse(data)[0]

BE = BinaryEncodings()