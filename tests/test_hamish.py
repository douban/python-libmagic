import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import hamish


PATH = os.path.realpath(__file__).rsplit('/', 1)[0]


class TestHamish(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(hamish.__version__)

    def test_gz(self):
        with open(os.path.join(PATH, 'files', 'test.gz')) as f:
            b = f.read()
            type = hamish.from_buffer(b, mime=True)
            self.assertEqual(type, 'application/x-gzip')
            type = hamish.from_buffer(b)
            self.assertEqual(type, 'gzip compressed data, was "test", '
                             'last modified: Sun Jun 29 09:32:52 2008,'
                             ' from Unix')

    def test_pdf(self):
        with open(os.path.join(PATH, 'files', 'test.pdf')) as f:
            b = f.read()
            type = hamish.from_buffer(b, mime=True)
            self.assertEqual(type, 'application/pdf')
            type = hamish.from_buffer(b)
            self.assertEqual(type, 'PDF document, version 1.2')

    def test_pyc(self):
        with open(os.path.join(PATH, 'files', 'magic.pyc')) as f:
            b = f.read()
            type = hamish.from_buffer(b, mime=True)
            self.assertEqual(type, 'binary')
            type = hamish.from_buffer(b)
            self.assertEqual(type, 'python 2.4 byte-compiled')

    # FIXME: always None ?
    def test_txt(self):
        with open(os.path.join(PATH, 'files', 'text.txt')) as f:
            b = f.read()
            type = hamish.from_buffer(b, mime=True)
            self.assertEqual(type, 'text/plain')
            type = hamish.from_buffer(b)
            self.assertEqual(type, 'ASCII text')

        with open(os.path.join(PATH, 'files', 'text-iso8859-1.txt')) as f:
            b = f.read()
            type = hamish.from_buffer(b, mime=True)
            self.assertEqual(type, 'text/plain')
            type = hamish.from_buffer(b)
            self.assertEqual(type, 'ISO-8859 text')

    def test_lambda(self):
        with open(os.path.join(PATH, 'files', b'\xce\xbb')) as f:
            b = f.read()
            type = hamish.from_buffer(b, mime=True)
            self.assertEqual(type, 'text/plain')
            type = hamish.from_buffer(b)
            self.assertEqual(type, 'ASCII text')

    def test_mime_encodings(self):
        m = hamish.open(mime_encoding=True)

        with open(os.path.join(PATH, 'files', 'text.txt')) as f:
            b = f.read()
            type = m.from_buffer(b)
            self.assertEqual(type, 'us-ascii')

        with open(os.path.join(PATH, 'files', 'text-iso8859-1.txt')) as f:
            b = f.read()
            type = m.from_buffer(b)
            self.assertEqual(type, 'iso-8859-1')

    def test_keep_going(self):
        path = os.path.join(PATH, 'files', 'keep-going.jpg')

        m = hamish.open(mime=True)
        type = m.from_file(path)
        # FIXME: should be application/octet-stream ?
        self.assertEqual(type, 'image/jpeg')

        m = hamish.open(mime=True, keep_going=True)
        type = m.from_file(path)
        self.assertEqual(type, 'image/jpeg')


if __name__ == '__main__':
    unittest.main()
