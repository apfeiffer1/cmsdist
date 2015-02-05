### RPM external py2-pycurl 7.19.5.1
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: http://pycurl.sourceforge.net/download/pycurl-%realversion.tar.gz
Requires: python curl openssl py2-pyopenssl py2-setuptools

%prep
%setup -n pycurl-%realversion

%build
python setup.py build --with-ssl --openssl-dir=${OPENSSL_ROOT} 

%install

python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
# Remove documentation.
%define drop_files %i/share

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
