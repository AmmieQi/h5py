
"""
    Attributes testing module

    Covers all operations which access the .attrs property, with the
    exception of data read/write and type conversion.  Those operations
    are tested by module test_attrs_data.
"""

import numpy as np

from common import TestCase, ut

from h5py.highlevel import File

class BaseAttrs(TestCase):

    def setUp(self):
        self.f = File(self.mktemp(), 'w')

    def tearDown(self):
        if self.f:
            self.f.close()

class TestAccess(BaseAttrs):

    """
        Feature: Attribute creation/retrieval via special methods
    """

    def test_create(self):
        """ Attribute creation by direct assignment """
        self.f.attrs['a'] = 4.0
        self.assertEqual(self.f.attrs.keys(), ['a'])
        self.assertEqual(self.f.attrs['a'], 4.0)

        self.f.attrs['b'] = 'b'
        self.assertEqual(self.f.attrs['b'], 'b')

    def test_overwrite(self):
        """ Attributes are silently overwritten """
        self.f.attrs['a'] = 4.0
        self.f.attrs['a'] = 5.0
        self.assertEqual(self.f.attrs['a'], 5.0)

    def test_rank(self):
        """ Attribute rank is preserved """
        self.f.attrs['a'] = (4.0, 5.0)
        self.assertEqual(self.f.attrs['a'].shape, (2,))
        self.assertArrayEqual(self.f.attrs['a'], np.array((4.0,5.0)))

    def test_single(self):
        """ Attributes of shape (1,) don't become scalars """
        self.f.attrs['a'] = np.ones((1,))
        out = self.f.attrs['a']
        self.assertEqual(out.shape, (1,))
        self.assertEqual(out[()], 1)

    def test_access_exc(self):
        """ Attempt to access missing item raises KeyError """
        with self.assertRaises(KeyError):
            self.f.attrs['a']


class TestDelete(BaseAttrs):

    """
        Feature: Deletion of attributes using __delitem__
    """

    def test_delete(self):
        """ Deletion via "del" """
        self.f.attrs['a'] = 4.0
        self.assertIn('a', self.f.attrs)
        del self.f.attrs['a']
        self.assertNotIn('a', self.f.attrs)

    def test_delete_exc(self):
        """ Attempt to delete missing item raises KeyError """
        with self.assertRaises(KeyError):
            del self.f.attrs['a']


class TestUnicode(BaseAttrs):

    """
        Feature: Attributes can be accessed via Unicode or byte strings
    """

    def test_ascii(self):
        """ Access via pure-ASCII byte string """
        self.f.attrs[b"ascii"] = 42
        out = self.f.attrs[b"ascii"]
        self.assertEqual(out, 42)

    def test_raw(self):
        """ Access via non-ASCII byte string """
        name = b"non-ascii\xfe"
        self.f.attrs[name] = 42
        out = self.f.attrs[name]
        self.assertEqual(out, 42)

    def test_unicode(self):
        """ Access via Unicode string with non-ascii characters """
        name = u"Omega \u03A9"
        self.f.attrs[name] = 42
        out = self.f.attrs[name]
        self.assertEqual(out, 42)
