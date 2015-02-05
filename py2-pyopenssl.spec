### RPM external py2-pyopenssl 0.14
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source: https://pypi.python.org/packages/source/p/pyOpenSSL/pyOpenSSL-%realversion.tar.gz
# md5=8579ff3a1d858858acfba5f046a4ddf7
Requires: python openssl py2-setuptools

%prep
%setup -n pyOpenSSL-%realversion

cat >> setup.cfg <<CMS_EOF
[build_ext]
include_dirs = $OPENSSL_ROOT/include
library_dirs = $OPENSSL_ROOT/lib
CMS_EOF

%build
python setup.py build 

%install
mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}

python setup.py install --single-version-externally-managed --record=/dev/null --skip-build --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

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
