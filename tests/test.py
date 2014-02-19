import magic
f = open('test.py')
b = f.read()
f.close()

m = magic.open(magic.MIME_TYPE)
assert m.from_buffer(b) == 'text/plain'
