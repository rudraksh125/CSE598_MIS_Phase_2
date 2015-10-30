#https://pypi.python.org/pypi/lzw/

import lzw

mybytes = lzw.readbytes("../README.md")
lessbytes = lzw.compress(mybytes)
lzw.writebytes("../lzw_encoded.txt", lessbytes)
print lessbytes.__sizeof__()
newbytes = b"".join(lzw.decompress(lzw.readbytes("../lzw_encoded.txt")))
decoded = open("../lzw_decoded.txt", 'w')
decoded.write(newbytes)
print newbytes
print newbytes.__sizeof__()
# oldbytes = b"".join(lzw.readbytes("../README.md"))
# print oldbytes
# print oldbytes == newbytes