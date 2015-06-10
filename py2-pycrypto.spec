### RPM external py2-pycrypto 2.6.1 
%define downloadn pycrypto
Requires: python gmp
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
Source: https://pypi.python.org/packages/source/p/pycrypto/pycrypto-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i

find %{i} -name '*.egg-info' -exec rm {} \;

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
