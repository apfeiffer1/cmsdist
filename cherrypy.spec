### RPM external cherrypy 3.2.6
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/source/C/CherryPy/CherryPy-3.2.6.tar.gz#md5=6902b972b82d3724e7b55f6504b2ac74
Requires: python
# Patch0: cherrypy-upload
# Patch1: cherrypy-trailers
# Patch2: cherrypy-report-all-bytes
Patch0: cherrypy-fixssl

%prep
%setup -n CherryPy-%realversion
# perl -p -i -e 's/import profile/import cProfile as profile/' cherrypy/lib/profiler.py
# %patch0 -p1
# %patch1 -p1
# %patch2 -p1
%patch0 -p1

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/cherryd; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
