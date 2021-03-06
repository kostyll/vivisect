import unittest

from vivisect.symboliks.common import *
from vivisect.symboliks.expression import symexp

class TestReduceCase(unittest.TestCase):
    '''
    tests the reduction of asts consisting of add's and sub's if widths are
    the same.
    '''
    def assertReduce(self, s1, s2):
        sym1 = symexp(s1).reduce()
        sym2 = symexp(s2)
        self.assertEqual(str(sym1),str(sym2))

    def assertNotReduce(self, s1, s2):
        sym1 = symexp(s1).reduce()
        sym2 = symexp(s2)
        self.assertNotEqual(str(sym1),str(sym2))

    def test_symboliks_reduce_and_consts(self):
        self.assertReduce('255 & 255','255')

    def test_symboliks_reduce_op_and(self):
        self.assertReduce('(foo & 0xff) & 0xff','foo & 0xff')
        self.assertReduce('(0xff & foo) & 0xff','foo & 0xff')
        self.assertReduce('0xff & (foo & 0xff)','foo & 0xff')
        self.assertReduce('0xff & (0xff & foo)','foo & 0xff')

        self.assertReduce('foo & 0','0')
        self.assertReduce('0 & foo','0')

        # reduce & with 0 regarless of width
        self.assertReduce('foo[1] & 0','0')
        self.assertReduce('0[1] & foo','0')

        # reduce & umax of foo to just foo
        self.assertReduce('foo[1] & 0xff','foo')
        self.assertReduce('foo[2] & 0xffff','foo')
        self.assertReduce('foo[4] & 0xffffffff','foo')

        self.assertNotReduce('foo[4] & 0xff','foo')
        self.assertNotReduce('foo[4] & 0xffff','foo')

    def test_symboliks_reduce_op_xor(self):
        self.assertReduce('foo ^ foo', '0')
        self.assertReduce('foo ^ 0', 'foo')

    def test_symboliks_reduce_op_mul(self):
        self.assertReduce('foo * 0','0')
        self.assertReduce('foo * 1','foo')
        #self.assertReduce('(foo / 2) * 2','foo')
        #self.assertReduce('(foo / 2) * 10','foo * 5')
        self.assertReduce('(foo * 10) / 2','foo * 5')
        self.assertReduce('(foo * 10) * 2','foo * 20')

    def test_symboliks_reduce_op_divmul(self):
        pass

    def test_symboliks_reduce_op_div(self):
        self.assertReduce('0 / foo','0')
        self.assertReduce('foo / foo','1')

    def test_symboliks_reduce_op_rshift(self):
        self.assertReduce('0 >> foo','0')
        self.assertReduce('foo >> 0','foo')

    def test_symboliks_reduce_op_lshift(self):
        self.assertReduce('0 << foo','0')
        self.assertReduce('foo << 0','foo')

    def test_symboliks_reduce_op_pow(self):
        self.assertReduce('0 ** foo','0')
        self.assertReduce('1 ** foo','1')
        self.assertReduce('foo ** 0','1')

    def test_symboliks_reduce_op_addsub(self):
        self.assertReduce('(foo + 255) + 10','foo + 265')
        self.assertReduce('(255 + foo) + 10','foo + 265')
        self.assertReduce('(255 + foo) + 10','foo + 265')
        self.assertReduce('(foo - 10) + 255','foo + 245')
        self.assertReduce('(255 - foo) + 10','(0 - foo) + 265')
        self.assertReduce('(foo + 255) - 10','foo + 245')
        self.assertReduce('(foo - 255) - 10','foo - 265')
        self.assertReduce('255 - (foo - 10)','265 - foo')
        self.assertReduce('255 - (foo + 10)','245 - foo')
        self.assertReduce('255 - (10 - foo)','foo + 245')
        self.assertReduce('(foo + 255) + (bar + 10)','(foo + bar) + 265')
        self.assertReduce('(foo - 10) + (bar + 255)','(bar + foo) + 245')
        self.assertReduce('(foo - 255) + (bar - 10)','(foo + bar) - 265')
        self.assertReduce('20 - (10 - eax)', 'eax + 10')
        self.assertReduce('(foo + 255) - (bar + 10)','(foo - bar) + 245')
        self.assertReduce('(foo + 255) - (10 + bar)','(foo - bar) + 245')
        self.assertReduce('(foo + 255) + (bar - 10)','(foo + bar) + 245')
        self.assertReduce('(foo + 255) + (10 - bar)','(foo - bar) + 265')
        self.assertReduce('(foo - 255) - (bar + 10)','(foo - bar) - 265')
        self.assertReduce('(255 - foo) - (bar + 10)','(( 0 - foo ) - bar) + 245')
        self.assertReduce('(foo + 255) - (bar - 10)','(foo - bar) + 265')
        self.assertReduce('(foo - 255) - (bar - 275)','(foo - bar) + 20')
        self.assertReduce('foo + 0','foo')
        self.assertReduce('0 + foo','foo')
        self.assertReduce('0 + 0','0')
        self.assertReduce('2 + 2','4')
        self.assertReduce('2 - 2','0')
        self.assertReduce('foo + (0 - bar)','foo - bar')
        self.assertReduce('foo + (0 + bar)','foo + bar')
        self.assertReduce('foo - (0 + bar)','foo - bar')
        self.assertReduce('0 - (0 - foo)','foo')
        self.assertReduce('0 + (0 + foo)','foo')
        self.assertReduce('0 - (0 + foo)','0 - foo')

