### RPM cms conddb-webtools 2.6
## NOCOMPILER
# with cmsBuild, change the above version only when a new tool is added
Source: none

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

Requires: cherrypy
Requires: py2-jinja
Requires: py2-pycurl
Requires: py2-sqlalchemy
Requires: py2-cx-oracle
Requires: py2-cjson
Requires: py2-lint
Requires: py2-pyopenssl
Requires: py2-django
Requires: python-ldap

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull icc-cxxcompiler icc-ccompiler icc-f77compiler boost_serialization boost_iostreams

%prep

%build

%install
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


