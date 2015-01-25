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

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
