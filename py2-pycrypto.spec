### RPM external py2-pycrypto 2.6.1 
%define downloadn pycrypto
Requires: python gmp
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
Source: https://pypi.python.org/packages/source/p/pycrypto/pycrypto-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%realversion
%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`
