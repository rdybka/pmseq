#!/bin/sh

# - clears the tree so we can do "git add ." (I know, I know)
# - regenerates the wrapper for libvht
# - don't run without swig3 installed
# - also uses black and astyle

rm -f *.snap *.so *.o libcvht/*.so
rm -f libcvht/*.o
rm -rf __pycache__
rm -rf vht/__pycache__
rm -rf libvht/__pycache__
rm -rf build
rm -f dist/*.gz
rm -f MANIFEST
rm -rf libvht/*.pyc
rm -rf vht/*.pyc
rm -rf dist
rm -rf vht.egg-info
rm -f libcvht/libcvht_wrap.c

cd libcvht
./beautify.sh
cd ..
black vht/*.py libvht/*.py
swig -python libcvht/libcvht.h
mv libcvht/libcvht.py .
snapcraft clean

