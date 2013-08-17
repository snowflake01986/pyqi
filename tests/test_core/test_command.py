#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from unittest import TestCase, main
from pyqi.core.command import Parameter, ParameterCollection, Command
from pyqi.core.exception import (IncompetentDeveloperError, 
                                 UnknownParameterError, 
                                 MissingParameterError)

class CommandTests(TestCase):
    def setUp(self):
        class stubby(Command):
            Parameters = ParameterCollection([
                            Parameter('a',int,'', Required=True),
                            Parameter('b',int,'', Required=False, Default=5)])
            def run(self, **kwargs):
                return {}
        self.stubby = stubby

    def test_init(self):
        """Jog the init"""
        c = Command()
        self.assertEqual(len(c.Parameters), 0)
        with self.assertRaises(NotImplementedError):
            _ = c()

    def test_subclass_init(self):
        """Exercise the subclassing"""
        class foo(Command):
            Parameters = ParameterCollection([Parameter('a', str, 'help1',
                                                        Required=True),
                                              Parameter('b', str, 'help2',
                                                        Required=False)])
            def run(self, **kwargs):
                return {}

        obs = foo()

        self.assertEqual(len(obs.Parameters), 2)
        self.assertEqual(obs.run(bar={'a':10}), {})

    def test_validate_kwargs(self):
        stub = self.stubby()
        kwargs = {'a':10, 'b':20}
        
        # should work
        stub._validate_kwargs(kwargs)

        kwargs = {'b':20}
        self.assertRaises(MissingParameterError, stub._validate_kwargs, kwargs)

    def test_set_defaults(self):
        stub = self.stubby()
        kwargs = {'a':10}
        exp = {'a':10,'b':5}
        
        stub._set_defaults(kwargs)

        self.assertEqual(kwargs, exp)

class ParameterTests(TestCase):
    def test_init(self):
        """Jog the init"""
        obj = Parameter('a', str, 'help', Required=False)
        self.assertEqual(obj.Name, 'a')
        self.assertEqual(obj.DataType, str)
        self.assertEqual(obj.Description, 'help')
        self.assertEqual(obj.Required, False)
        self.assertEqual(obj.Default, None)
        self.assertEqual(obj.DefaultDescription, None)
        self.assertRaises(IncompetentDeveloperError, Parameter, 'a', str,
                          'help', True, 'x')

class ParameterCollectionTests(TestCase):
    def test_init(self):
        """Jog the init"""
        params = [Parameter('a', str, 'help', Required=False),
                  Parameter('b', float, 'help2', Required=True)]
        obj = ParameterCollection(params)

        self.assertEqual(obj.Parameters, params)
        self.assertEqual(obj['a'], params[0])
        self.assertEqual(obj['b'], params[1])

        # Duplicate Parameter names.
        params.append(Parameter('a', int, 'help3'))
        with self.assertRaises(IncompetentDeveloperError):
            _ = ParameterCollection(params)


class ParameterCollectionTests(TestCase):
    def setUp(self):
        self.pc = ParameterCollection([Parameter('foo',str, 'help')])
    
    def test_getitem(self):
        self.assertRaises(UnknownParameterError, self.pc.__getitem__, 'bar')
        self.assertEqual(self.pc['foo'].Name, 'foo') # make sure we can getitem

    def test_setitem(self):
        self.assertRaises(TypeError, self.pc.__setitem__, 'bar', 10)

if __name__ == '__main__':
    main()
