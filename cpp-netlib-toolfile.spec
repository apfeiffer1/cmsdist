### RPM external cpp-netlib-toolfile 1.0
Requires: cpp-netlib
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cpp-netlib.xml
<tool name="cpp-netlib" version="@TOOL_VERSION@">
  <info url="http://cpp-netlib.org/index.html"/>
  <lib name="cppnetlib-client-connections"/>
  <lib name="cppnetlib-server-parsers"/>
  <lib name="cppnetlib-uri"/>
  <client>
    <environment name="CPP_NETLIB_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CPP_NETLIB_BASE/lib64"/>
    <environment name="INCLUDE" default="$CPP_NETLIB_BASE/include"/>
  </client>
  <runtime name="CPP_NETLIB_PARAM_PATH" value="$CPP_NETLIB_BASE"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$CPP_NETLIB_BASE/include" type="path"/>
  <runtime name="BOOST_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
