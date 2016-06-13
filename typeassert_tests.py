# coding: utf-8
import unittest
from typeassert import *


class TestTypeassertBypass(unittest.TestCase):

  def test_bypass(self):

    disable_typeassert()

    typeassert(12, 'str') # typeassert not activated
    typeassert(12, 'int', True) # bypass activation
    with self.assertRaises(TypeassertException):
      typeassert(12, 'str', True)

    activate_typeassert()


activate_typeassert() # else it does nothing

class TestTypeassert(unittest.TestCase):

  def test_int(self):
    typeassert(12, 'int')
    typeassert(-12, 'int')
    with self.assertRaises(TypeassertException):
      typeassert(12, 'str')
    with self.assertRaises(TypeassertException):
      typeassert('bla', 'int')

  def test_floats(self):
    typeassert(1.2, 'float')
    typeassert(1.2, 'float')
    with self.assertRaises(TypeassertException):
      typeassert(12.0, 'str')
    with self.assertRaises(TypeassertException):
      typeassert('bla', 'float')

  def test_tuples(self):
    typeassert((1,2,3), '(int,int,int)')
    typeassert((1,2,3), '(int..)')
    typeassert((1.,2.), '(float..)') # handled as '(1. ..)'
    typeassert((1, "deux"), '()')
    with self.assertRaises(TypeassertException):
      typeassert((1,2,3), '(float)')

  def test_array(self):
    typeassert([1,2,3], '[int,int,int]')
    typeassert([1,2,3], '[int..]')
    typeassert([1, "deux"], '[]')
    with self.assertRaises(TypeassertException):
      typeassert([1,2,3], 'int')
    with self.assertRaises(TypeassertException): # spec is not of same type
      typeassert(1, '[int]')
    with self.assertRaises(TypeassertException): # spec is longer
      typeassert([1,2], '[int,int,int]')

  def test_dict(self):
    typeassert({11:2},         '{int:int}')
    typeassert({11:2, 12: 3},  '{}')
    typeassert({11:2, 12: 3},  '{int:int}')
    typeassert({11:2, 12: 3},  '{int:int, int:int}') #should fail, though...

  def test_set(self):
    typeassert({11, 2},  '{int}')
    typeassert({11, 2, 123},  '{}')
    with self.assertRaises(TypeassertException):
      typeassert({11, 's'},  '{int}')
    with self.assertRaises(TypeassertException):
      typeassert([11, 's'],  '{int}')

  def test_wildcard(self):
    typeassert(12, '*')

  def test_missing_item(self):
    with self.assertRaises(TypeassertException):
      typeassert((12), '(*, int)')

  def test_dotdot(self):
    typeassert(['a'], '[str..]')
    with self.assertRaises(TypeassertException):
      typeassert(['a'], '[str...]')
    typeassert(['a', 'b', 'c'], '[str..]')
    with self.assertRaises(TypeassertException):
      typeassert([12, 'a', 'b', 'c'], '[int, str..]')
    with self.assertRaises(TypeassertException):
      typeassert([12, 13, 'b', 'c'], '[int, int, str..]')
    with self.assertRaises(TypeassertException):
      typeassert([12, 13, 'b', 'c'], '[int.., str..]')

  def test_named_variables(self):
    typeassert(12, 'my_name@int')
    typeassert([12], '[my_other_name@int]')
    typeassert((12,'s'), '(a@int, b@str)')
    typeassert(12, 'my-name@int')
    typeassert(12, 'my9@int')
    with self.assertRaises(TypeassertException):
      typeassert(12, 'my/name@int')
    with self.assertRaises(TypeassertException):
      typeassert(12, 'my name@int')


  def test_mixes(self):
    #typeassert({11: (2,3), 12: (4,"5")}, '{ int: (int,*)}')
    typeassert([(2, "asdf"),(-12, "asfwe"),(1,"")], "[(int,str)..]")
    with self.assertRaises(TypeassertException):
      typeassert({11: (2,3), 12: (4,"5")}, '{ int: (int,int)}')

  def test_multiple(self):
    typeassert((2, "asdf"), "(int,str)", (2, "asdf"), "(int,str)")


if __name__ == '__main__':
  import examples
  unittest.main()
