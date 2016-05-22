import re


class AddressException(Exception):
    pass


class Address(object):


  def __init__(self, address):
    self.postCodeRegexp = re.compile(r"\b[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][ABD-HJLNP-UW-Z]{2}\b")
    try:
      self.address = str(str(address).strip().split('\n')[0])
    except Exception as e:
      raise AddressException("Could not format address: %s" % address)


  def post_code(self):
    """Get the post code"""
    try:
      return re.findall(self.postCodeRegexp, self.address)[0].replace(' ', '')
    except Exception as e:
        raise AddressException("Could not extract post code from address: %s" % self.address)


  def full(self):
    """Get the full address"""
    try:
      return ", ".join(self.address.split(', ')[0:-1]).lower().title()
    except Exception as e:
        raise AddressException("Could not format full address: %s" % self.address)