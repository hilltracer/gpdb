Name: arenadata_db
Version: 6.21.1_arenadata36
Release: alt1

Summary: Analytical database based on Greenplum-DB
License: Apache-2.0
Group: Databases
Url: https://github.com/arenadata/gpdb.git
Source: %name-%version.tar

# Git submodules
Source1: source.tar 
Source2: ext.tar
Source3: googletest.tar

# Automatically added by buildreq on Thu Nov 10 2022
# optimized out: bash4 glibc-kernheaders-generic glibc-kernheaders-x86 gnu-config libcrypt-devel libgpg-error libsasl2-3 libstdc++-devel libuuid-devel libxerces-c perl python-modules python-modules-distutils python2-base sh4
BuildRequires: bzlib-devel flex gcc-c++ libapr1-devel libcurl-devel libevent-devel libreadline-devel libxerces-c-devel libyaml-devel libzstd-devel python-devel zlib-devel
BuildPreReq: perl-Pod-Usage
AutoReqProv: nopython nopython3

%description
Arenadata DB (ADB) is an analytical, distributed database built on the
open source MPP system Greenplum. It is designed to store and process
large amounts of information - up to tens of petabytes. 
With Arenadata DB, you'll build a robust, scalable enterprise data
warehouse that grows with your needs.

%prep
%setup
tar -xf %SOURCE1 -C gpAux/extensions/pgbouncer
tar -xf %SOURCE2 -C gpMgmt/bin/pythonSrc
tar -xf %SOURCE3 -C gpcontrib/gpcloud/test

# Remove compiler options that cause an error on fresh GCC.
sed -i '/-std=c++98/d' src/backend/gpopt/gpopt.mk
sed -i '/-std=gnu++98/d' src/backend/gporca/gporca.mk
# Delete wrong rpath
sed -i '/rpathdir = $(python_libdir)/d' src/pl/plpython/Makefile
# Change `python` to `python2` in scripts.
# Attention! When updating the package, you need to make sure that no new
# scripts with the "python" call appeared in the upstream.
sed -i 's/python -c/python2 -c/' gpMgmt/bin/gpinitsystem
sed -i 's/python helpers_test.py/python2 helpers_test.py/' src/test/isolation2/Makefile
sed -i 's/python gpconfig_modules/python2 gpconfig_modules/; s/python setup.py/python2 setup.py/; s/shell python -c/shell python2 -c/; s/python -m unittest/python2 -m unittest/' gpMgmt/bin/Makefile
sed -i 's/python parse_perf_results.py/python2 parse_perf_results.py/' src/test/performance/Makefile
sed -i 's/python -m pytest/python2 -m pytest/' gpMgmt/bin/gpload_test/Makefile
sed -i 's/python "/python2 "/' gpMgmt/bin/gpload.bat
sed -i 's/python TEST_REMOTE.py/python2 TEST_REMOTE.py/' concourse/scripts/ic_gpdb_remote_windows.bat
sed -i 's/python .\/sql_isolation_testcase.py/python2 .\/sql_isolation_testcase.py/' src/test/isolation2/isolation2_main.c
sed -i 's/python -c/python2 -c/' src/tools/msvc/Mkvcbuild.pm
sed -i 's/python -c/python2 -c/' gpMgmt/bin/gpcheckperf
sed -i 's/python -c/python2 -c/' gpMgmt/bin/gpmemwatcher
sed -i 's/PYTHON="python"/PYTHON="python2"/' config/ax_python_module.m4
sed -i 's/python -c/python2 -c/' gpMgmt/bin/gppylib/operations/buildMirrorSegments.py
sed -i 's/python -c/python2 -c/' gpMgmt/bin/gppylib/commands/gp.py
sed -i 's/python \/tmp\/pid_background_script.py/python2 \/tmp\/pid_background_script.py/' gpMgmt/test/behave/mgmt_utils/steps/mgmt_utils.py  
sed -i 's/python -c/python2 -c/' gpMgmt/test/behave/mgmt_utils/steps/mirrors_mgmt_utils.py
sed -i 's/python -c/python2 -c/' gpMgmt/bin/gppylib/operations/unix.py 
sed -i 's/python -c/python2 -c/' gpAux/gpperfmon/src/gpmon/gpperfmon.sql 
sed -i 's/python -c/python2 -c/' src/backend/catalog/gp_toolkit.sql
sed -i 's/\/usr\/bin\/python /\/usr\/bin\/python2 /' concourse/scripts/unit_tests_gporca.bash
# Change `python` to `python2` in shebangs.
find . -type f ! -path '*/\.*' -name '*.py' -exec sed \
	-i -e 's/\/usr\/bin\/env python.*/\/usr\/bin\/env python2/g' -e 's/\/bin\/python.*/\/bin\/python2/g' {} + \
-or ! -path '*/\.*' -type f ! -name '*.*' -exec sed \
	-i 's/\/usr\/bin\/env python.*/\/usr\/bin\/env python2/g' {} +

%build
%define adb_dir %_usr/%_lib/%name
%autoreconf
%configure \
    --prefix=%adb_dir  \
    --exec-prefix=%adb_dir  \
    --bindir=%adb_dir/bin \
    --sbindir=%adb_dir/sbin \
    --sysconfdir=/etc \
    --datadir=%adb_dir/share \
    --libdir=%adb_dir/lib \
    --includedir=%adb_dir/include \
    --libexecdir=%adb_dir/libexec \
    --localstatedir=/var/lib \
    --sharedstatedir=/var/lib \
    --mandir=%adb_dir/share/man \
    --infodir=%adb_dir/share/info \
    --with-python \
    --disable-gpcloud \
    --enable-debug-extensions \
    --enable-cassert \
    --enable-depend \
    CFLAGS="-Wno-error=nonnull-compare -Wno-error=deprecated-copy"
%make_build -s

%install
%makeinstall_std -s

%files
%adb_dir
# Medicine for "ERROR: static library packaging violation (contains both .a and .so)"
%exclude %adb_dir/lib/libecpg.so
%exclude %adb_dir/lib/libecpg_compat.so
%exclude %adb_dir/lib/libgppc.so
%exclude %adb_dir/lib/libpgtypes.so
%exclude %adb_dir/lib/libpq.so

%changelog
* Thu Nov 10 2022 Denis Garsh <hilltracer@altlinux.org> 6.21.1_arenadata36-alt1
- 6.21.1_arenadata36
