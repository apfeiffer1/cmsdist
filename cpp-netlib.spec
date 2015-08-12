### RPM external cpp-netlib 0.11.1

Source: http://storage.googleapis.com/cpp-netlib-downloads/%{realversion}/%{n}-%{realversion}-final.tar.gz
Source1: http://cern.ch/pfeiffer/FindBoost.cmake
Patch0: cpp-netlib-fixFindBoost

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11 -O2
%endif

BuildRequires: cmake boost
Requires: boost openssl

%prep
%setup -n %{n}-%{realversion}-final
%patch0 -p1 

%build

mkdir -p ./cmake/boost
cp %{SOURCE1} ./cmake/boost/

export CMAKE_PREFIX_PATH=${BOOST_ROOT}:${CMAKE_PREFIX_PATH}

#-ap NOTE: it is mandatory that the lib gets compiled with the 
#          same settings for -std in the CMAKE_CXX_FLAGS as for
#          boost, otherwise execution will "hang forever" in
#          the body(request) call ...
cmake ../cpp-netlib-%{realversion}-final \
  --debug-output \
  -DCMAKE_CXX_FLAGS="-std=c++11" \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCPP-NETLIB_BUILD_SHARED_LIBS=ON \
  -DBoost_DIR="${PWD}/cmake/boost/" \
  -DCMAKE_MODULE_PATH="${PWD}/cmake/boost/"

make %{makeprocesses} VERBOSE=1


%install
make install

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib

%post
# %{relocateConfig}bin/libpng-config
