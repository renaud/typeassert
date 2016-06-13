import re
# global status, whether to perform type checking
# by default, do nothing (to preserve cpu time)
typeassert_active = False # by default, pass

'''disable typeassert (default)'''
def disable_typeassert():
  global typeassert_active
  typeassert_active = False

'''configure/activate typeassert to emmit errors'''
def activate_typeassert():
  global typeassert_active
  typeassert_active = True

class TypeassertException(Exception):
    pass


# all known types
valid_spec = re.compile(r'^(int|str|float|bool|self|None|[,\.: \*\?\{\}\[\]\(\)])+$').match
# removes all named variables (letters, numbers and _-)
remove_named_vars = re.compile(r'[a-z_\-0-9]+@').sub


def _parse_spec(spec):
  spec_novars = remove_named_vars('', spec)

  if not valid_spec(spec_novars):
    raise TypeassertException('spec can only contain int, float, str, bool, self, None and a combination of ,.: *?{{}}[]() but was >>{}<<'.format(spec))

  # transform the spec from [(int,str)..] to [(1,'m'), '..']
  spec_p = str(spec_novars)\
    .replace('int',   '1')\
    .replace('float', '1.0')\
    .replace('str',   '"m"')\
    .replace('bool',  'True')\
    .replace('*',     '"ignore"')\
    .replace('?',     '"optional"')\
    .replace('self',  '"ignore"')\
    .replace('..', ',".."')
  #print 'spec_p >{}<'.format(spec_p)

  try:
    print 'EVAL', spec_p, "EVALUATED", eval(spec_p)
    return eval(spec_p)
  except:
    raise TypeassertException('could not parse spec >>{}<< (resolved to >>{}<<)'.format(spec, spec_p))

'''
main function to check the type of the provided object, given a spec
'''
def typeassert(*args):
  if typeassert_active or bypass: # by default, pass
    assert len(args) % 2 == 0, 'there should be an even number of arguments, but was {}'.format(args)
    for i in xrange(0, len(args), 2):
      obj, spec = args[i], args[i + 1]
      _check(obj, _parse_spec(spec), obj, spec) # recursive


def _check(o, spec, o_original, spec_original):
  print '_check: obj=', o, 'spec=', spec

  if spec != "ignore": # bypass check if spec is wildcard ('?', self, None)

    # check type equality

    # start with a few exceptions: str is fine for unicode...
    if type(o) is unicode and type(spec) is str:
      pass
    elif type(o) is set and str(spec) == '{}':  # exception for empty set
      pass                                    # (else its eval is considered a dict)
    elif type(o) != type(spec):
      raise TypeassertException("Type of '{}' must be of type {} but was of type {} (object: '{}'; spec: '{}')".format(o, type(spec), type(o), o_original, spec_original))

    # handle data structures recursively
    elif type(o) is tuple or type(o) is list:

      if len(spec) == 0: # empty spec, e.g. () or [] -> ignore (type equivalence was already tested above)
        pass

      elif len(spec) == 2 and spec[1] == '..': # spec of type dotdot (e.g. int..)
        # --> repeat spec[0] for every item of o
        [_check(x, spec[0], o_original, spec_original) for i, x in enumerate(o)]

      else: # spec is fixed length, e.g. [int,int,float,str]

        for s in spec: # check that spec does not contain ..
          if s == '..':
            raise TypeassertException('Illegal spec {}; can only contain .. at the second entry of a tuple or list, e.g. [int..] or [str..]'.format(spec_original))

        if len(spec) != len(o):
          raise TypeassertException("Object length of {} does not match spec {} (object: '{}'; spec: '{}')".format(o, spec, o_original, spec_original))


        [_check(x, spec[i], o_original, spec_original) for i, x in enumerate(o)]

    elif type(o) is dict:
      if len(spec) == 0: # empty spec {} -> ignore
        pass
      elif len(spec) == 1:
        key_spec, value_spec = spec.popitem()
        for key, value in o.items():
          _check(key,   key_spec, o_original, spec_original)
          _check(value, value_spec, o_original, spec_original)
      else:
        raise TypeassertException('Spec {} for dict should only contain 1 single item, e.g. "{{1: \'s\'}}"'.format(spec_original))

    elif type(o) is set:
      assert len(spec) == 1, 'spec {} for set should only contain 1 single item, e.g. "{{1}}"'.format(spec_original)
      set_spec = spec.pop() # the single item in this set spec
      for i in o:
        _check(i, set_spec, o_original, spec_original)
