%define _refman_version 5.0
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl):	Prosty, lekki ale potê¿ny, osadzalny jêzyk programowania
Name:		lua50
Version:	5.0.2
Release:	3
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	e515b9a12d129eaa52f88b9686e0b6a1
Source1:	http://www.lua.org/ftp/refman-%{_refman_version}.ps.gz
# Source1-md5:	4b0cedef4880bf925da9537520d93b57
Patch0:		lua5-link.patch
URL:		http://www.lua.org/
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua = %{version}
Obsoletes:	lua < 4.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

This version has compiled in support for dynamic libraries in baselib.

%description -l pl
Lua to jêzyk programowania o du¿ych mo¿liwo¶ciach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest te¿ czêsto u¿ywany jako
samodzielny jêzyk ogólnego przeznaczenia. £±czy prost± proceduraln±
sk³adniê (podobn± do Pascala) z potê¿nymi konstrukcjami opisu danych
bazuj±cymi na tablicach asocjacyjnych i rozszerzalnej sk³adni. Lua ma
dynamiczny system typów, interpretowany z bytecodu i automatyczne
zarz±dzanie pamiêci± z od¶miecaczem, co czyni go idealnym do
konfiguracji, skryptów i szybkich prototypów.

Ta wersja ma wkompilowan± obs³ugê ³adowania dynamicznych bibliotek.

%package libs
Summary:	lua 5.0.x libraries
Summary(pl):	Biblioteki lua 5.0.x
Group:		Development/Languages

%description libs
lua 5.0.x libraries.

%description libs -l pl
Biblioteki lua 5.0.x.

%package devel
Summary:	Header files for Lua
Summary(pl):	Pliki nag³ówkowe dla Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua-devel = %{version}

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%description devel -l pl
Pliki nag³ówkowe potrzebne do w³±czenia Lua do programów w C/C++ oraz
dokumentacja samego jêzyka.

%package static
Summary:	Static Lua libraries
Summary(pl):	Biblioteki statyczne Lua
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Provides:	lua-static = %{version}

%description static
Static Lua libraries.

%description static -l pl
Biblioteki statyczne Lua.

%prep
%setup -q -n lua-%{version}
cp -f %{SOURCE1} refman.ps.gz

%patch0 -p1

%build
%{__make} all so sobin \
	CC="%{__cc}" \
	MYCFLAGS="%{rpmcflags} -fPIC" \
	EXTRA_DEFS="-DPIC -D_GNU_SOURCE"

rm -f test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/lua,%{_datadir}/lua}

%{__make} soinstall install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua50 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1

# change name from lua to lua50
for i in $RPM_BUILD_ROOT%{_bindir}/* ; do mv $i{,50} ; done
mv $RPM_BUILD_ROOT%{_libdir}/liblua{,50}.a
mv $RPM_BUILD_ROOT%{_libdir}/liblualib{,50}.a
mv $RPM_BUILD_ROOT%{_mandir}/man1/lua{,50}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/luac{,50}.1

rm $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -s liblua.so.5.0 $RPM_BUILD_ROOT%{_libdir}/liblua50.so
ln -s liblualib.so.5.0 $RPM_BUILD_ROOT%{_libdir}/liblualib50.so
rm -f doc/*.1

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc refman.ps.gz doc test
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/lua50

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
