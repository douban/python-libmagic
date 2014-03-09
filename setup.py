# -*- coding: utf-8 -*-
import os
import tarfile
from subprocess import Popen, PIPE
from setuptools import setup, Extension, find_packages

# setuptools DWIM monkey-patch madness
# http://mail.python.org/pipermail/distutils-sig/2007-September/thread.html#8204
import sys
if 'setuptools.extension' in sys.modules:
    m = sys.modules['setuptools.extension']
    m.Extension.__dict__ = m._Extension.__dict__

PYTHON3K = sys.version_info[0] > 2

cwd = os.path.dirname(os.path.realpath(__file__))
vendor_path = os.path.join(cwd, 'vendor')

def excute(command_list, shell=False, wait=False):
    popen = Popen(command_list, stdout=PIPE, stderr=PIPE, shell=shell)
    if wait:
        popen.wait()
    stdoutdata, stderrdata = popen.communicate()
    if popen.returncode != 0:
        print(stderrdata)
        sys.exit()

def extract(file):
    t = tarfile.open(file, mode='r:gz')
    t.extractall()

os.chdir(vendor_path)

# extract file
extract('file-5.17.tar.gz')

# extract zlib
extract('zlib-1.2.8.tar.gz')

libmagic_path = os.path.join(vendor_path, 'file-5.17')
os.chdir(libmagic_path)

# build libmagic
excute(['patch -p0 < ../file-locale-5.17.patch'], shell=True, wait=True)

excute(['./configure', '--prefix=%s' % vendor_path, '--disable-shared',
         '--enable-static', '--with-pic'])

excute(['make', '-C', 'src', 'install'])

excute(['make', '-C', 'magic', 'install'])

# build libz
libz_path = os.path.join(vendor_path, 'zlib-1.2.8')
os.chdir(libz_path)
excute(['./configure', '--prefix=%s' % vendor_path, '--static'])

excute(['make', 'install'])

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
    ext_modules=[Extension("_magic",
                           ["src/magic.pyx"],
                           include_dirs=['vendor/include'],
                           library_dirs=['vendor/lib'],
                           libraries=["magic_embed", "z_embed"])],
    py_modules=['hamish'],
    packages=find_packages(),
    package_data={'': ['misc/magic.mgc']},
    include_package_data=True,
    zip_safe=False,
    tests_require=['mock'] + [] if PYTHON3K else ['unittest2'],
    test_suite="tests" if PYTHON3K else "unittest2.collector",
    data_files=[('misc', ['vendor/share/misc/magic.mgc'])],
)
