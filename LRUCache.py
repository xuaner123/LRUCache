'''
LRU Cache

Caches are a key element in scaling a system. One popular form of cache is called a Least Recently Used Cache (http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used). Your task is to implement a cache that can be tested against a series of inputs. These actions should define an API you use for the cache object.

Your cache should store simple key/value strings of length up to 10 characters. It should also have a customizable upper bound to the number of keys that can be stored in the cache at any time. You do not have to be thread safe.

Possible Inputs:

BOUND    :  Set the upper bound. If the cache size is currently greater than this number, then extra entries must be removed following the LRU policy
SET   :  Set the value of this key
GET   :  Get the value of this key and prints to stdout.
PEEK   :  Gets the value of the key but does not mark it as being used. Prints the value to standard out.
DUMP  :  Prints the current state of the cache as a list of key/value pairs in alphabetical order by key.

Input Format:

First line of input contains an integer N,the number of commands.

The following N lines each describe a command.

Note: The first command will always be BOUND.

Output Format:

Print the appropriate outputs for GET , PEEK and DUMP commands. In case for GET/PEEK command if the key does not exist in the cache just output the string "NULL"(quotes are for clarity).

Sample Input

8
BOUND 2
SET a 2
SET b 4
GET b
PEEK a
SET c 5
GET a
DUMP

Sample Output

4
2
NULL
b 4
c 5

Constraints:

Total number of lines in input will be no more than 1,000,000(10^6)

Note: There may be DUMP commands scattered throughout the input file.
'''

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
      to_evict = sorted(self._cache.values())[0]
      del self._cache[to_evict.key()]

  def bound(self, size):
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

  def __init__(self, cache, input_commands):
    self._cache = cache
    self._commands = ['BOUND', 'SET', 'GET', 'PEEK', 'DUMP']
    self._input_commands = input_commands

  def execute_all(self):

    for cmd in self._input_commands:
      cmd = cmd.split(' ')
      
      cache_command = cmd[0]
      arguments = cmd[1:]

      self.__execute(cache_command, arguments) 

  def __execute(self, cmd, args = []):
    if cmd not in self._commands:
      raise InvalidCacheCommand()

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

  input_commands = [line.strip() for line in sys.stdin.readlines() if line != '\n'][1:]

  cache = LRUCache()

  command_executor = CacheCommandExecutor(cache, input_commands)

  command_executor.execute_all() 
