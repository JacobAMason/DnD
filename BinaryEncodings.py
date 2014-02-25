# BinaryEncodings.py
# Below are some Binary encodings for various client/server interactions
import struct

class BinaryEncodings:
    """
    returns True or False based on whether or not data is one of the binary encodings.
    """
    def __init__(self):
        self.DISCONNECT = struct.pack("!3s", bytes("DIS", "utf-8"))
        self.CONNECT    = struct.pack("!3s", bytes("CON", "utf-8"))
        self.MESSAGE    = struct.pack("!3s", bytes("MSG", "utf-8"))

    def get_type(self, num):
        """
        Evaluates a number and returns it's 
        """

    def unpack(self, astr, fmt="!3ss*"):
        """
        Return struct.unpack(fmt, astr) with the optional single * in fmt replaced with
        the appropriate number, given the length of astr.
        """
        # http://stackoverflow.com/a/7867892/190597
        try:
            return struct.unpack(fmt, astr)
        except struct.error:
            flen = struct.calcsize(fmt.replace('*', ''))
            alen = len(astr)
            idx = fmt.find('*')
            before_char = fmt[idx-1]
            n = int((alen-flen)/struct.calcsize(before_char)+1)
            fmt = ''.join((fmt[:idx-1], str(n), before_char, fmt[idx+1:]))
            return struct.unpack(fmt, astr)

BE = BinaryEncodings()