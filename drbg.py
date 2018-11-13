import sys
import hashlib
import binascii

class SHAKE(object):
  """ Deterministic "random" generator using SHAKE
      Some code from: https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Random/_UserFriendlyRNG.py
  """

  def __init__(self, seed):
    self.closed = False
    hash_from_seed = hashlib.sha512(seed.encode()).digest()
    self.dk = hashlib.shake_256(hash_from_seed).digest(1000000)
    self.pos = 0
    self.bytes_read = 0

  def close(self):
    pass

  def flush(self):
    pass

  def read(self, N):
    """Return N bytes from the RNG."""
    if not isinstance(N, (int)):
      raise TypeError("an integer is required")
    if N < 0:
      raise ValueError("cannot read to end of infinite stream")
    if self.pos + N > len(self.dk):
      raise ValueError("cannot read past the end of the stream, not enough entropy, please retry")

    # Create the "random" data
    r = self.dk[self.pos : self.pos + N]
    self.bytes_read = self.bytes_read + len(r)

    # set the position to our latest read byte
    self.pos = self.pos + N
    return r

