### RPM cms conddb-webtools 2.2
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

%define skipreqtools jcompiler lhapdfwrapfull lhapdffull icc-cxxcompiler icc-ccompiler icc-f77compiler boost_serialization boost_iostreams

%prep

%build

%install


