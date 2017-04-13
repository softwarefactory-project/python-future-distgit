Name: python-future
Summary: Easy, clean, reliable Python 2/3 compatibility
Version: 0.16.0
Release: 3%{?dist}
License: MIT
Group: Applications/Engineering
URL: http://python-future.org/
Source0: https://github.com/PythonCharmers/python-future/archive/v%{version}.tar.gz#/python-future-%{version}.tar.gz
BuildArch: noarch

##https://github.com/PythonCharmers/python-future/issues/165
Patch0: %{name}-skip_tests_with_connection_errors.patch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: numpy
BuildRequires: python-requests
BuildRequires: pytest

%description
%{name} is the missing compatibility layer between Python 2 and
Python 3. It allows you to use a single, clean Python 3.x-compatible
codebase to support both Python 2 and Python 3 with minimal overhead.

It provides ``future`` and ``past`` packages with backports and forward
ports of features from Python 3 and 2. It also comes with ``futurize`` and
``pasteurize``, customized 2to3-based scripts that helps you to convert
either Py2 or Py3 code easily to support both Python 2 and 3 in a single
clean Py3-style codebase, module by module.

%prep
%setup -qc

mv python-future-%{version} python2
pushd python2
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'
%patch0 -p0
popd

%build
pushd python2
CFLAGS="%{optflags}" %{__python2} setup.py build --executable="%{__python2} -s"
popd

%install
pushd python2
CFLAGS="%{optflags}" %{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cp -p $RPM_BUILD_ROOT%{_bindir}/futurize $RPM_BUILD_ROOT%{_bindir}/python%{python2_version}-futurize
cp -p $RPM_BUILD_ROOT%{_bindir}/pasteurize $RPM_BUILD_ROOT%{_bindir}/python%{python2_version}-pasteurize

for i in futurize futurize-2 futurize-%{python2_version}; do
  touch $i
  install -p $i $RPM_BUILD_ROOT%{_bindir}
  ln -sf %{_bindir}/python%{python2_version}-futurize $RPM_BUILD_ROOT%{_bindir}/$i
done
for i in pasteurize pasteurize-2 pasteurize-%{python2_version}; do
  touch $i
  install -p $i $RPM_BUILD_ROOT%{_bindir}
  ln -sf %{_bindir}/python%{python2_version}-pasteurize $RPM_BUILD_ROOT%{_bindir}/$i
done
sed -i -e '/^#!\//, 1d' $RPM_BUILD_ROOT%{python2_sitelib}/future/backports/test/pystone.py
popd

%files
%{!?_licensedir:%global license %doc}
%doc python2/README.rst
%license python2/LICENSE.txt
%{_bindir}/futurize
%{_bindir}/futurize-2*
%{_bindir}/pasteurize
%{_bindir}/pasteurize-2*
%{_bindir}/python%{python2_version}-futurize
%{_bindir}/python%{python2_version}-pasteurize
%{python2_sitelib}/future/
%{python2_sitelib}/past/
%{python2_sitelib}/libfuturize/
%{python2_sitelib}/libpasteurize/
%{python2_sitelib}/tkinter/
%{python2_sitelib}/_dummy_thread/
%{python2_sitelib}/_markupbase/
%{python2_sitelib}/_thread/
%{python2_sitelib}/builtins/
%{python2_sitelib}/copyreg/
%{python2_sitelib}/html/
%{python2_sitelib}/http/
%{python2_sitelib}/queue/
%{python2_sitelib}/reprlib/
%{python2_sitelib}/socketserver/
%{python2_sitelib}/winreg/
%{python2_sitelib}/xmlrpc/
%{python2_sitelib}/*.egg-info

%changelog
* Thu Apr 13 2017 Tristan Cacqueray <tdecacqu@redhat.com> 0.16.0-3
- Only support python2, and rename to python-future for sf reqs

* Tue Dec 13 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-2
- BR Python2 dependencies unversioned on epel6

* Tue Dec 13 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-1
- Update to 0.16.0

* Wed Aug 17 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.15.2-10
- Rebuild for Python 3.5.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.15.2-7
- Renamed Python2 package

* Thu Dec 10 2015 Antonio Trande <sagitterATfedoraproject.org> - 0.15.2-6
- SPEC file adapted to recent guidelines for Python

* Fri Nov 13 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-5
- Rebuild

* Fri Nov 13 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-4
- Python3 tests temporarily disabled with Python35

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 0.15.2-3 - Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 14 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-2
- Patch0 updated

* Fri Sep 11 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-1
- Update to 0.15.2

* Wed Sep 02 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-4
- Added patch to exclude failed tests (patch0)

* Wed Aug 26 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-3
- Added python-provides macro

* Thu Jul 30 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-2
- Fixed Python3 packaging on Fedora
- Removed configparser backport (patch1)

* Tue Jul 28 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-1
- Initial build
