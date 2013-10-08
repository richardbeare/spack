"""
These version tests were taken from the RPM source code.
We try to maintain compatibility with RPM's version semantics
where it makes sense.
"""
import unittest
from spack.version import *


class VersionsTest(unittest.TestCase):

    def assert_ver_lt(self, a, b):
        a, b = ver(a), ver(b)
        self.assertTrue(a < b)
        self.assertTrue(a <= b)
        self.assertTrue(a != b)
        self.assertFalse(a == b)
        self.assertFalse(a > b)
        self.assertFalse(a >= b)


    def assert_ver_gt(self, a, b):
        a, b = ver(a), ver(b)
        self.assertTrue(a > b)
        self.assertTrue(a >= b)
        self.assertTrue(a != b)
        self.assertFalse(a == b)
        self.assertFalse(a < b)
        self.assertFalse(a <= b)


    def assert_ver_eq(self, a, b):
        a, b = ver(a), ver(b)
        self.assertFalse(a > b)
        self.assertTrue(a >= b)
        self.assertFalse(a != b)
        self.assertTrue(a == b)
        self.assertFalse(a < b)
        self.assertTrue(a <= b)


    def assert_in(self, needle, haystack):
        self.assertTrue(ver(needle) in ver(haystack))


    def assert_not_in(self, needle, haystack):
        self.assertFalse(ver(needle) in ver(haystack))


    def assert_canonical(self, canonical_list, version_list):
        self.assertEqual(ver(canonical_list), ver(version_list))


    def assert_overlaps(self, v1, v2):
        self.assertTrue(ver(v1).overlaps(ver(v2)))


    def assert_no_overlap(self, v1, v2):
        self.assertFalse(ver(v1).overlaps(ver(v2)))


    def test_two_segments(self):
        self.assert_ver_eq('1.0', '1.0')
        self.assert_ver_lt('1.0', '2.0')
        self.assert_ver_gt('2.0', '1.0')


    def test_three_segments(self):
        self.assert_ver_eq('2.0.1', '2.0.1')
        self.assert_ver_lt('2.0',   '2.0.1')
        self.assert_ver_gt('2.0.1', '2.0')


    def test_alpha(self):
        # TODO: not sure whether I like this.  2.0.1a is *usually*
        # TODO: less than 2.0.1, but special-casing it makes version
        # TODO: comparison complicated.  See version.py
        self.assert_ver_eq('2.0.1a', '2.0.1a')
        self.assert_ver_gt('2.0.1a', '2.0.1')
        self.assert_ver_lt('2.0.1',  '2.0.1a')


    def test_patch(self):
        self.assert_ver_eq('5.5p1',  '5.5p1')
        self.assert_ver_lt('5.5p1',  '5.5p2')
        self.assert_ver_gt('5.5p2',  '5.5p1')
        self.assert_ver_eq('5.5p10', '5.5p10')
        self.assert_ver_lt('5.5p1',  '5.5p10')
        self.assert_ver_gt('5.5p10', '5.5p1')


    def test_num_alpha_with_no_separator(self):
        self.assert_ver_lt('10xyz',   '10.1xyz')
        self.assert_ver_gt('10.1xyz', '10xyz')
        self.assert_ver_eq('xyz10',   'xyz10')
        self.assert_ver_lt('xyz10',   'xyz10.1')
        self.assert_ver_gt('xyz10.1', 'xyz10')


    def test_alpha_with_dots(self):
        self.assert_ver_eq('xyz.4', 'xyz.4')
        self.assert_ver_lt('xyz.4', '8')
        self.assert_ver_gt('8',     'xyz.4')
        self.assert_ver_lt('xyz.4', '2')
        self.assert_ver_gt('2',     'xyz.4')


    def test_nums_and_patch(self):
        self.assert_ver_lt('5.5p2', '5.6p1')
        self.assert_ver_gt('5.6p1', '5.5p2')
        self.assert_ver_lt('5.6p1', '6.5p1')
        self.assert_ver_gt('6.5p1', '5.6p1')


    def test_rc_versions(self):
        self.assert_ver_gt('6.0.rc1', '6.0')
        self.assert_ver_lt('6.0',     '6.0.rc1')


    def test_alpha_beta(self):
        self.assert_ver_gt('10b2', '10a1')
        self.assert_ver_lt('10a2', '10b2')


    def test_double_alpha(self):
        self.assert_ver_eq('1.0aa', '1.0aa')
        self.assert_ver_lt('1.0a',  '1.0aa')
        self.assert_ver_gt('1.0aa', '1.0a')


    def test_padded_numbers(self):
        self.assert_ver_eq('10.0001', '10.0001')
        self.assert_ver_eq('10.0001', '10.1')
        self.assert_ver_eq('10.1',    '10.0001')
        self.assert_ver_lt('10.0001', '10.0039')
        self.assert_ver_gt('10.0039', '10.0001')


    def test_close_numbers(self):
        self.assert_ver_lt('4.999.9', '5.0')
        self.assert_ver_gt('5.0',     '4.999.9')


    def test_date_stamps(self):
        self.assert_ver_eq('20101121', '20101121')
        self.assert_ver_lt('20101121', '20101122')
        self.assert_ver_gt('20101122', '20101121')


    def test_underscores(self):
        self.assert_ver_eq('2_0', '2_0')
        self.assert_ver_eq('2.0', '2_0')
        self.assert_ver_eq('2_0', '2.0')


    def test_rpm_oddities(self):
        self.assert_ver_eq('1b.fc17', '1b.fc17')
        self.assert_ver_lt('1b.fc17', '1.fc17')
        self.assert_ver_gt('1.fc17',  '1b.fc17')
        self.assert_ver_eq('1g.fc17', '1g.fc17')
        self.assert_ver_gt('1g.fc17', '1.fc17')
        self.assert_ver_lt('1.fc17',  '1g.fc17')


    # Stuff below here is not taken from RPM's tests and is
    # unique to spack
    def test_version_ranges(self):
        self.assert_ver_lt('1.2:1.4', '1.6')
        self.assert_ver_gt('1.6', '1.2:1.4')
        self.assert_ver_eq('1.2:1.4', '1.2:1.4')
        self.assertNotEqual(ver('1.2:1.4'), ver('1.2:1.6'))

        self.assert_ver_lt('1.2:1.4', '1.5:1.6')
        self.assert_ver_gt('1.5:1.6', '1.2:1.4')


    def test_contains(self):
        self.assert_in('1.3', '1.2:1.4')
        self.assert_in('1.2.5', '1.2:1.4')
        self.assert_in('1.3.5', '1.2:1.4')
        self.assert_in('1.3.5-7', '1.2:1.4')
        self.assert_not_in('1.1', '1.2:1.4')
        self.assert_not_in('1.5', '1.2:1.4')
        self.assert_not_in('1.4.2', '1.2:1.4')

        self.assert_in('1.2.8', '1.2.7:1.4')
        self.assert_in('1.2.7:1.4', ':')
        self.assert_not_in('1.2.5', '1.2.7:1.4')
        self.assert_not_in('1.4.1', '1.2.7:1.4')


    def test_in_list(self):
        self.assert_in('1.2', ['1.5', '1.2', '1.3'])
        self.assert_in('1.2.5', ['1.5', '1.2:1.3'])
        self.assert_in('1.5', ['1.5', '1.2:1.3'])
        self.assert_not_in('1.4', ['1.5', '1.2:1.3'])

        self.assert_in('1.2.5:1.2.7', [':'])
        self.assert_in('1.2.5:1.2.7', ['1.5', '1.2:1.3'])
        self.assert_not_in('1.2.5:1.5', ['1.5', '1.2:1.3'])
        self.assert_not_in('1.1:1.2.5', ['1.5', '1.2:1.3'])


    def test_ranges_overlap(self):
        self.assert_overlaps('1.2', '1.2')
        self.assert_overlaps('1.2.1', '1.2.1')
        self.assert_overlaps('1.2.1b', '1.2.1b')

        self.assert_overlaps('1.2:1.7', '1.6:1.9')
        self.assert_overlaps(':1.7', '1.6:1.9')
        self.assert_overlaps(':1.7', ':1.9')
        self.assert_overlaps(':1.7', '1.6:')
        self.assert_overlaps('1.2:', '1.6:1.9')
        self.assert_overlaps('1.2:', ':1.9')
        self.assert_overlaps('1.2:', '1.6:')
        self.assert_overlaps(':', ':')
        self.assert_overlaps(':', '1.6:1.9')


    def test_lists_overlap(self):
        self.assert_overlaps('1.2b:1.7,5', '1.6:1.9,1')
        self.assert_overlaps('1,2,3,4,5', '3,4,5,6,7')
        self.assert_overlaps('1,2,3,4,5', '5,6,7')
        self.assert_overlaps('1,2,3,4,5', '5:7')
        self.assert_overlaps('1,2,3,4,5', '3, 6:7')
        self.assert_overlaps('1, 2, 4, 6.5', '3, 6:7')
        self.assert_overlaps('1, 2, 4, 6.5', ':, 5, 8')
        self.assert_overlaps('1, 2, 4, 6.5', ':')
        self.assert_no_overlap('1, 2, 4', '3, 6:7')
        self.assert_no_overlap('1,2,3,4,5', '6,7')
        self.assert_no_overlap('1,2,3,4,5', '6:7')


    def test_canonicalize_list(self):
        self.assert_canonical(['1.2', '1.3', '1.4'],
                              ['1.2', '1.3', '1.3', '1.4'])

        self.assert_canonical(['1.2', '1.3:1.4'],
                              ['1.2', '1.3', '1.3:1.4'])

        self.assert_canonical(['1.2', '1.3:1.4'],
                              ['1.2', '1.3:1.4', '1.4'])

        self.assert_canonical(['1.3:1.4'],
                              ['1.3:1.4', '1.3', '1.3.1', '1.3.9', '1.4'])

        self.assert_canonical(['1.3:1.4'],
                              ['1.3', '1.3.1', '1.3.9', '1.4', '1.3:1.4'])

        self.assert_canonical(['1.3:1.5'],
                              ['1.3', '1.3.1', '1.3.9', '1.4:1.5', '1.3:1.4'])

        self.assert_canonical(['1.3:1.5'],
                              ['1.3, 1.3.1,1.3.9,1.4:1.5,1.3:1.4'])

        self.assert_canonical(['1.3:1.5'],
                              ['1.3, 1.3.1,1.3.9,1.4 : 1.5 , 1.3 : 1.4'])

        self.assert_canonical([':'],
                              [':,1.3, 1.3.1,1.3.9,1.4 : 1.5 , 1.3 : 1.4'])
