### RPM external py2-pyopenssl 0.11
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES

Source: https://launchpad.net/pyopenssl/main/%realversion/+download/pyOpenSSL-%realversion.tar.gz
Requires: python openssl

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
python setup.py install --prefix=%i
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
