### RPM external py2-pip 6.0.6
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: none
Requires: python

%prep

%build
DOWNLOAD_TOOL=$(basename $(which curl || which wget || echo "none"))
DOWNLOAD_FILE=https://bootstrap.pypa.io/get-pip.py

case "${DOWNLOAD_TOOL}" in
   curl)
      # cURL does not download empty files, touch file before downloading
      curl -L -O -k ${DOWNLOAD_FILE}
      ;;
   wget)
      wget --no-check-certificate --no-verbose ${DOWNLOAD_FILE}
      ;;
   none)
      echo "Unsupported download tool. Could not locate curl or wget. Contact package maintainer."
      exit 1
      ;;
esac

# wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py


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
