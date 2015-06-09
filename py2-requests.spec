### RPM external py2-requests 2.7.0
## INITENV +PATH PYTHONPATH %{i}/$PYTHON_LIB_SITE_PACKAGES

Source: https://pypi.python.org/packages/source/r/requests/requests-%{realversion}.tar.gz#md5=29b173fd5fa572ec0764d1fd7b527260
Requires: python 

%prep
%setup -n Requests-%{realversion}

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}

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
