import sys
import inspect
import heapq
import random


class Pair(object):
    """
    A utility class to represent pairs (ordering of the objects in the pair does not matter).
    It is used to represent mutexes (for both actions and propositions)
    """

    def __init__(self, a, b):
        """
        Constructor
        """
        self.a = a
        self.b = b

    def __eq__(self, other):
        if (self.a == other.a) & (self.b == other.b):
            return True
        if (self.b == other.a) & (self.a == other.b):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "(" + str(self.a) + "," + str(self.b) + ")"

    def __hash__(self):
        return hash(self.a) + hash(self.b)


def lookup(name, namespace):
    """
    Get a method or class from any imported module from its name.
    Usage: lookup(functionName, globals())
    """
    dots = name.count('.')
    if dots > 0:
        moduleName, objName = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(moduleName)
        return getattr(module, objName)
    else:
        modules = [obj for obj in namespace.values() if str(type(obj)) == "<type 'module'>"]
        options = [getattr(module, name) for module in modules if name in dir(module)]
        options += [obj[1] for obj in namespace.items() if obj[0] == name]
        if len(options) == 1: return options[0]
        if len(options) > 1: raise Exception('Name conflict for %s')
        raise Exception('%s not found as a method or class' % name)

