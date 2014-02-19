# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE
from setuptools import setup, Extension, find_packages

# setuptools DWIM monkey-patch madness
# http://mail.python.org/pipermail/distutils-sig/2007-September/thread.html#8204
import sys
if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__

cwd = os.path.dirname(os.path.realpath(__file__))
vendor_path = os.path.join(cwd, 'vendor')

os.chdir(vendor_path)

popen = Popen(['tar', '-zxvf', 'file-5.17.tar.gz'], stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

popen = Popen(['tar', '-zxvf', 'zlib-1.2.8.tar.gz'], stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

libmagic_path = os.path.join(vendor_path, 'file-5.17')
os.chdir(libmagic_path)

# build libmagic
popen = Popen(['./configure', '--prefix=%s' % vendor_path, '--disable-shared',
               '--enable-static', '--with-pic'],
              stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

popen = Popen(['make', '-C', 'src', 'install'], stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

popen = Popen(['make', '-C', 'magic', 'install'], stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

# build libz
libz_path = os.path.join(vendor_path, 'zlib-1.2.8')
os.chdir(libz_path)
popen = Popen(['./configure', '--prefix=%s' % vendor_path, '--static'],
              stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

popen = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE)
stdoutdata, stderrdata = popen.communicate()
if popen.returncode != 0:
    print(stderrdata)
    sys.exit()

# prepare embed lib
os.rename(os.path.join(vendor_path, 'lib', 'libmagic.a'),
          os.path.join(vendor_path, 'lib', 'libmagic_embed.a'))
os.rename(os.path.join(vendor_path, 'lib', 'libz.a'),
          os.path.join(vendor_path, 'lib', 'libz_embed.a'))

os.chdir(cwd)

setup(
    name="python-libmagic",
    version="0.0.1",
    license="revised BSD",
    description="A wrapper for libmagic with static build.",
    author="XTao",
    author_email='xutao881001@gmail.com',
    setup_requires=['setuptools_cython'],
    install_requires=['cython>=0.20'],
    ext_modules=[Extension("magic",
                           ["src/magic.pyx"],
                           include_dirs=['vendor/include'],
                           library_dirs=['vendor/lib'],
                           libraries=["magic_embed", "z_embed"])],
    py_modules=['magic'],
    packages=find_packages(),
    package_data={'': ['misc/magic.mgc']},
    include_package_data=True,
    zip_safe=False,
    data_files=[('misc', ['vendor/share/misc/magic.mgc'])],
)
