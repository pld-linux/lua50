#
# Conditional build:
%bcond_with	luastatic	# build dietlibc-based static lua version
%bcond_with	default_lua	# build as default lua (symlinks to nil suffix)
#
Summary:	A simple lightweight powerful embeddable programming language
Summary(pl.UTF-8):	Prosty, lekki ale potężny, osadzalny język programowania
Name:		lua50
Version:	5.0.3
%define	refman_ver	5.0
Release:	5
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	feee27132056de2949ce499b0ef4c480
Source1:	http://www.lua.org/ftp/refman-%{refman_ver}.ps.gz
# Source1-md5:	4b0cedef4880bf925da9537520d93b57
Patch0:		lua5-link.patch
Patch1:		%{name}-Makefile.patch
URL:		http://www.lua.org/
%{?with_luastatic:BuildRequires:       dietlibc-static}
Requires:	%{name}-libs = %{version}-%{release}
%if %{with default_lua}
Provides:	lua = %{version}
Obsoletes:	lua < %{version}
%endif
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
Summary:	Lua 5.0.x shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Lua 5.0.x
Group:		Libraries

%description libs
Lua 5.0.x shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Lua 5.0.x.

%package devel
Summary:	Header files for Lua
Summary(pl.UTF-8):	Pliki nagłówkowe dla Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
%if %{with default_lua}
Provides:	lua-devel = %{version}
Obsoletes:	lua-devel < %{version}
%endif

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
%if %{with default_lua}
Provides:	lua-static = %{version}
Obsoletes:	lua-static < %{version}
%endif

%description static
Static Lua libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Lua.

%package luastatic
Summary:	Static Lua interpreter
Summary(pl.UTF-8):	Statycznie skonsolidowany interpreter lua
Group:		Development/Languages
%if %{with default_lua}
Provides:	lua-luastatic = %{version}
Obsoletes:	lua-luastatic < %{version}
%endif

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
	CC="diet %{__cc}" \
	MYCFLAGS="%{rpmcflags} -fPIC -Os" \
	EXTRA_DEFS="-DPIC -D_GNU_SOURCE"

%{__mv} bin bin.static

%{__make} clean
%endif

%{__make} -j1 all so sobin \
	CC="%{__cc}" \
	MYCFLAGS="%{rpmcflags} -fPIC" \
	EXTRA_DEFS="-DPIC -D_GNU_SOURCE"

%{__rm} test/{lua,luac}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} soinstall install \
	INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} \
	INSTALL_BIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTALL_INC=$RPM_BUILD_ROOT%{_includedir}/lua5.0 \
	INSTALL_LIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1

# change name from lua to lua5.0
for i in $RPM_BUILD_ROOT%{_bindir}/lua* ; do
	%{__mv} ${i}{,5.0}
done
%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblua{,5.0}.a
%{__mv} $RPM_BUILD_ROOT%{_libdir}/liblualib{,5.0}.a

ln -sf liblua.so.5.0 $RPM_BUILD_ROOT%{_libdir}/liblua5.0.so
ln -sf liblualib.so.5.0 $RPM_BUILD_ROOT%{_libdir}/liblualib5.0.so

%if %{with luastatic}
install bin.static/lua $RPM_BUILD_ROOT%{_bindir}/lua5.0.static
install bin.static/luac $RPM_BUILD_ROOT%{_bindir}/luac5.0.static
%endif

# create pkgconfig file
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua5.0.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}/lua5.0
libdir=%{_libdir}
interpreter=%{_bindir}/lua5.0
compiler=%{_bindir}/luac5.0

Name: Lua
Description: An extension programming language
Version: %{version}
Cflags: -I%{_includedir}
Libs: -L%{_libdir} -llua5.0 -llualib5.0 -ldl -lm
EOF

%if %{with default_lua}
for f in lua luac ; do
	ln -sf ${f}5.0 $RPM_BUILD_ROOT%{_bindir}/${f}
	echo ".so ${f}5.0.1" >$RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
%if %{with luastatic}
	ln -sf ${f}5.0.static $RPM_BUILD_ROOT%{_bindir}/${f}.static
%endif
done
ln -sf liblua5.1.a $RPM_BUILD_ROOT%{_libdir}/liblua.a
ln -sf liblualib5.1.a $RPM_BUILD_ROOT%{_libdir}/liblualib.a
ln -sf lua5.1 $RPM_BUILD_ROOT%{_includedir}/lua
ln -sf lua5.1.pc $RPM_BUILD_ROOT%{_pkgconfigdir}/lua.pc
%else
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{lua,lualib}.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua5.0
%attr(755,root,root) %{_bindir}/luac5.0
%{_mandir}/man1/lua5.0.1*
%{_mandir}/man1/luac5.0.1*
%if %{with default_lua}
%attr(755,root,root) %{_bindir}/lua
%attr(755,root,root) %{_bindir}/luac
%{_mandir}/man1/lua.1*
%{_mandir}/man1/luac.1*
%endif

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/liblua.so.5.0
%attr(755,root,root) %{_libdir}/liblualib.so.5.0

%files devel
%defattr(644,root,root,755)
%doc refman.ps.gz doc test
%attr(755,root,root) %{_libdir}/liblua5.0.so
%attr(755,root,root) %{_libdir}/liblualib5.0.so
%{_includedir}/lua5.0
%{_pkgconfigdir}/lua5.0.pc
%if %{with default_lua}
%attr(755,root,root) %{_libdir}/liblua.so
%attr(755,root,root) %{_libdir}/liblualib.so
%{_includedir}/lua
%{_pkgconfigdir}/lua.pc
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/liblua5.0.a
%{_libdir}/liblualib5.0.a
%if %{with default_lua}
%{_libdir}/liblua.a
%{_libdir}/liblualib.a
%endif

%if %{with luastatic}
%files luastatic
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua5.0.static
%attr(755,root,root) %{_bindir}/luac5.0.static
%if %{with default_lua}
%attr(755,root,root) %{_bindir}/lua.static
%attr(755,root,root) %{_bindir}/luac.static
%endif
%endif
