### RPM external boost 1.38.0
%define boostver _%(echo %realversion | tr . _)
Source: http://internap.dl.sourceforge.net/sourceforge/%{n}/%{n}%{boostver}.tar.gz
%define online %(case %cmsplatf in *onl_*_*) echo true ;; esac)

Requires: boost-build python bz2lib
%if "%online" != "true"
Requires: zlib
%endif

%prep
%setup -n %{n}%{boostver}

%build
# Note that some targets will fail to build (the test programs have
# missing symbols), causing darwin to fail to link and bjam to return
# an error.  So ignore the exit code from bjam on darwin to avoid
# RPM falsely detecting a problem.
PV="PYTHON_VERSION=$(echo $PYTHON_VERSION | sed 's/\.[0-9]*-.*$//')"
PR="PYTHON_ROOT=$PYTHON_ROOT"

# The following line assumes a version of the form x.y.z-XXXX, where the
# "-XXXX" part represents some CMS rebuild of version x.y.z
BZ2LIBR="BZIP2_LIBPATH=$BZ2LIB_ROOT/lib"
BZ2LIBI="BZIP2_INCLUDE=$BZ2LIB_ROOT/include"

%if "%online" != "true"
ZLIBR="ZLIB_LIBPATH=$ZLIB_ROOT/lib"
ZLIBI="ZLIB_INCLUDE=$ZLIB_ROOT/include"

case $(uname) in
  Darwin )  bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR -sTOOLS=darwin --toolset=darwin || true ;;
  * )       bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$ZLIBR -sTOOLS=gcc ;;
esac
%else
bjam %makeprocesses -s$PR -s$PV -s$BZ2LIBR -s$BZ2LIBI -sTOOLS=gcc
%endif

%install
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
#no debug libs...
#mkdir -p %i/lib/debug
mkdir %i/lib
#(cd bin/boost; find libs -path "libs/*/debug/*.$so" -exec cp {} %i/lib/debug \;)
# Perhaps the following could be done with a wildcard for the darwin/gcc dir
case %cmsplatf in 
  osx*) 
    (cd bin.v2; find libs -path "libs/*/build/darwin*/release/*.$so*" -exec cp  {} %i/lib/. \;)
    ;;
  * )
    (cd bin.v2; find libs -path "libs/*/build/gcc*/release/*.$so*" -exec cp  {} %i/lib/. \;)
    ;;
esac

find boost -name '*.[hi]*' -print |
  while read f; do
    mkdir -p %i/include/$(dirname $f)
    install -c $f %i/include/$f
  done
find libs -name '*.py' -print |
  while read f; do
    mkdir -p %i/lib/$(dirname $f)
    install -c $f %i/lib/$f
  done

# Do all manipulation with files before creating symbolic links:
perl -p -i -e "s|^#!.*python|/usr/bin/env python|" $(find %{i}/lib %{i}/bin)
#strip %i/lib/*.$so 

for l in `find %i/lib -name "*.$so.*"`
do
  ln -s `basename $l` `echo $l | sed -e "s|[.]$so[.].*|.$so|"`
done

(cd %i/lib/libs/python/pyste/install; python setup.py install --prefix=%i)

getLibName()
{
  libname=`find %i/lib -name "libboost_$1*mt*.$so" -exec basename {} \;`
  echo $libname | sed -e 's|[.][^-]*$||;s|^lib||'
}

export BOOST_THREAD_LIB=`getLibName thread`
export BOOST_SIGNALS_LIB=`getLibName signals`
export BOOST_FILESYSTEM_LIB=`getLibName filesystem`
export BOOST_SYSTEM_LIB=`getLibName system`
export BOOST_PROGRAM_OPTIONS_LIB=`getLibName program_options`
export BOOST_PYTHON_LIB=`getLibName python`
export BOOST_REGEX_LIB=`getLibName regex`

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# boost toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_THREAD_LIB@">
<lib name="@BOOST_SIGNALS_LIB@">
<Client>
 <Environment name=BOOST_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$BOOST_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$BOOST_BASE/include"></Environment>
</Client>
<use name=sockets>
<Runtime name=LD_LIBRARY_PATH value="$BOOST_BASE/lib" type=path>
<Runtime name=CMSSW_FWLITE_INCLUDE_PATH value="$BOOST_BASE/include" type=path>
</Tool>
EOF_TOOLFILE

# boost_filesystem toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_filesystem
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_filesystem version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_FILESYSTEM_LIB@">
<use name=boost_system>
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_system toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_system
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_system version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_SYSTEM_LIB@">
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_program_options toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_program_options
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_program_options version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_PROGRAM_OPTIONS_LIB@">
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_python toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_python
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_python version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_PYTHON_LIB@">
<Client>
 <Environment name=BOOST_PYTHON_BASE default="%i"></Environment>
 <Environment name=PYSTE_EXEC default="$BOOST_PYTHON_BASE/lib/python2.4/site-packages/Pyste/pyste.py"></Environment>
 <Environment name=LIBDIR default="$BOOST_PYTHON_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$BOOST_PYTHON_BASE/include"></Environment>
</Client>
<use name=elementtree>
<use name=gccxml>
<use name=python>
</Tool>
EOF_TOOLFILE

# boost_regex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_regex
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_regex version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_REGEX_LIB@">
<use name=boost>
</Tool>
EOF_TOOLFILE

# boost_signals toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_signals
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=boost_signals version=%v>
<info url="http://www.boost.org"></info>
<lib name="@BOOST_SIGNALS_LIB@">
<use name=boost>
</Tool>
EOF_TOOLFILE

perl -p -i -e 's|\@([^@]*)\@|$ENV{$1}|g' %i/etc/scram.d/*

%post
%{relocateConfig}etc/scram.d/boost
%{relocateConfig}etc/scram.d/boost_filesystem
%{relocateConfig}etc/scram.d/boost_program_options
%{relocateConfig}etc/scram.d/boost_python
%{relocateConfig}etc/scram.d/boost_regex
%{relocateConfig}etc/scram.d/boost_signals
