import sys

class CacheEntryException(Exception):
  def __init__(self, value = 'Key and Value must be both strings and less than 10 characters'):
    self._value = value

  def __str__(self):
    return repr(self._value)

class InvalidCacheCommand(Exception):
  def __init__(self, value = 'Command cannot be executed as it is not supported'):
    self._value = value

  def __str__(self):
    return repr(self._value)

class Cacheable:
  '''
  Represents an immutable cachable object to be inserted into and retrieved from an LRUCache.
  Every time a get operation is issued on the particular object, the object's age increases.
  This keeps track of how recently it was used.
  '''
  def __init__(self, key, value):
    self._key = key
    self._value = value
    self._age = 0

  def key(self):
    return self._key

  def value(self):
    return self._value

  def age(self):
    self._age += 1

  def get_age(self):
    return self._age

  def __cmp__(self, obj):
    if obj == None:
      return -1
    if not isinstance(obj, Cacheable):
      return -1
    if self._age < obj.age():
      return -1
    if self._age == obj.age():
      return 0
    if self._age > obj.age():
      return 1

class LRUCache:
  '''
  Represents an LRUCache implementing the LRU Caching algorithm. Provides the standard API for
  an LRUCache as seen in the description above
  '''

  def __init__(self, size = 10):
    self._size = size
    self._key_set = []
    self._entry_set = []
    self._cache = {}

  def __check_entry_constraints(self, *args, **kwargs):
    check = True
    for arg in args:
      check = check and (type(arg) == str and len(arg) <= 10)
    return check

  def __check_and_evict(self):
    if len(self._cache.keys()) == self._size:
      to_evict = min(self._cache.values())
      del self._cache[to_evict.key()]

  def bound(self, size):
    if size < 0:
        print 'invalid BOUND size'
        sys.exit()
    else:
        self._size = size  

  def set(self, key, value):
    self.__check_and_evict()
    check = self.__check_entry_constraints(key, value)
    
    if not check:
      raise CacheEntryException()
    
    self._cache[key] = Cacheable(key, value)

  def __get_and_age(self, key, age):
    value = self._cache.get(key)

    if value != None:
      if age:
        value.age()
        self._cache[key] = value
      return value.value()

    return 'NULL'

  def get(self, key):
    print self.__get_and_age(key, True)

  def peek(self, key):
    print self.__get_and_age(key, False)

  def dump(self):
    keys = sorted(self._cache.keys())
    
    for key in keys:
      print key, self._cache[key].value()

class CacheCommandExecutor:

  def __init__(self, cache, input_commands=[]):
    self._cache = cache
    self._commands = ['BOUND', 'SET', 'GET', 'PEEK', 'DUMP']
    self._input_commands = input_commands

  def execute_all(self):

    for cmd in self._input_commands:
      cmd = cmd.split(' ')
      
      cache_command = cmd[0]
      arguments = cmd[1:]

      self.execute(cache_command, arguments) 

  def execute(self, cmd, args = []):
    if cmd not in self._commands:
      return

    if cmd == 'BOUND':
      self._cache.bound(int(args[0]))
    if cmd == 'SET':
      self._cache.set(args[0], args[1])
    if cmd == 'GET':
      self._cache.get(args[0])
    if cmd == 'PEEK':
      self._cache.peek(args[0])
    if cmd == 'DUMP':
      self._cache.dump()
 
if __name__ == '__main__':

  N = sys.stdin.readline()

  cache = LRUCache()
  command_executor = CacheCommandExecutor(cache)

  for line in sys.stdin:
    line = line.strip().split(' ')
    cmd, args = line[0], line[1:]

    command_executor.execute(cmd, args)
