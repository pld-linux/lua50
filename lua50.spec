#
# Conditional build:
%bcond_with	luastatic        # build dietlibc-based static lua version
#
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl.UTF-8):	Prosty, lekki ale potężny, osadzalny język programowania
Name:		lua50
Version:	5.0.3
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	feee27132056de2949ce499b0ef4c480
%define		_refman_version	5.0
Source1:	http://www.lua.org/ftp/refman-%{_refman_version}.ps.gz
# Source1-md5:	4b0cedef4880bf925da9537520d93b57
Patch0:		lua5-link.patch
Patch1:		%{name}-Makefile.patch
URL:		http://www.lua.org/
%{?with_luastatic:BuildRequires:       dietlibc-devel}
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

%description -l pl.UTF-8
Lua to język programowania o dużych możliwościach ale lekki,
przeznaczony do rozszerzania aplikacji. Jest też często używany jako
samodzielny język ogólnego przeznaczenia. Łączy prostą proceduralną
składnię (podobną do Pascala) z potężnymi konstrukcjami opisu danych
bazującymi na tablicach asocjacyjnych i rozszerzalnej składni. Lua ma
dynamiczny system typów, interpretowany z bytecodu i automatyczne
zarządzanie pamięcią z odśmiecaczem, co czyni go idealnym do
konfiguracji, skryptów i szybkich prototypów.

Ta wersja ma wkompilowaną obsługę ładowania dynamicznych bibliotek.

%package libs
Summary:	lua 5.0.x libraries
Summary(pl.UTF-8):	Biblioteki lua 5.0.x
Group:		Development/Languages

%description libs
lua 5.0.x libraries.

%description libs -l pl.UTF-8
Biblioteki lua 5.0.x.

%package devel
Summary:	Header files for Lua
Summary(pl.UTF-8):	Pliki nagłówkowe dla Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Provides:	lua-devel = %{version}

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do włączenia Lua do programów w C/C++ oraz
dokumentacja samego języka.

%package static
Summary:	Static Lua libraries
Summary(pl.UTF-8):	Biblioteki statyczne Lua
Group:		Development/Languages
Requires:	%{name}-devel = %{version}-%{release}
Provides:	lua-static = %{version}

%description static
Static Lua libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Lua.

%package luastatic
Summary:        Static Lua interpreter
Summary(pl.UTF-8):	Statycznie skonsolidowany interpreter lua
Group:		Development/Languages

%description luastatic
Static lua interpreter.

%description luastatic -l pl.UTF-8
Statycznie skonsolidowany interpreter lua.

%prep
%setup -q -n lua-%{version}
cp -f %{SOURCE1} refman.ps.gz
%patch0 -p1
%patch1 -p1

%build
%if %{with luastatic}
%{__make} all sobin \
	CC="%{_target_cpu}-dietlibc-gcc" \
	MYCFLAGS="%{rpmcflags} -fPIC" \
	EXTRA_DEFS="-DPIC -D_GNU_SOURCE"
mv bin bin.static
%{__make} clean
%endif

%{__make} -j1 all so sobin \
	CC="%{__cc}" \
	MYCFLAGS="%{rpmcflags} -fPIC" \
	EXTRA_DEFS="-DPIC -D_GNU_SOURCE"

rm -f test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/lua}

%{__make} soinstall install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua50 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1

# change name from lua to lua50
for i in $RPM_BUILD_ROOT%{_bindir}/* ; do mv ${i}{,50} ; done
mv $RPM_BUILD_ROOT%{_libdir}/liblua{,50}.a
mv $RPM_BUILD_ROOT%{_libdir}/liblualib{,50}.a

rm $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -s liblua.so.5.0 $RPM_BUILD_ROOT%{_libdir}/liblua50.so
ln -s liblualib.so.5.0 $RPM_BUILD_ROOT%{_libdir}/liblualib50.so

%if %{with luastatic}
install bin.static/lua $RPM_BUILD_ROOT%{_bindir}/lua50.static
install bin.static/luac $RPM_BUILD_ROOT%{_bindir}/luac50.static
%endif

# create pkgconfig file
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua50.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}/%{name}
libdir=%{_libdir}
interpreter=%{_bindir}/%{name}
compiler=%{_bindir}/luac50

Name: Lua
Description: An extension programming language
Version: %{version}
Cflags: -I%{_includedir}/%{name}
Libs: -L%{_libdir} -llua50 -llualib50 -ldl -lm
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua50
%attr(755,root,root) %{_bindir}/luac50
%{_mandir}/man1/lua50.1*
%{_mandir}/man1/luac50.1*

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc refman.ps.gz doc test
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/lua50
%{_pkgconfigdir}/lua50.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with luastatic}
%files luastatic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*static
%endif
