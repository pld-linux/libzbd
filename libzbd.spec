#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Library to control zoned block devices
Summary(pl.UTF-8):	Biblioteka do kontroli strefowych urządzeń blokowych
Name:		libzbd
Version:	2.0.2
Release:	1
License:	LGPL v3+ (library), GPL v3+ (tools)
Group:		Libraries
#Source0Download: https://github.com/westerndigitalcorporation/libzbd/releases
Source0:	https://github.com/westerndigitalcorporation/libzbd/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e003141516df60733ddc196ec0a8c530
URL:		https://github.com/westerndigitalcorporation/libzbd
%{?with_gui:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	linux-libc-headers >= 7:4.10
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libzbd is a library providing functions simplifying access to zoned
block device information and the execution of zone management
operations.

%description -l pl.UTF-8
libzbd to biblioteka udostępniająca funkcje upraszczające dostęp do
informacji o strefowych urządzeniach blokowych oraz wykonywanie
operacji związanych z zarządzaniem strefami.

%package devel
Summary:	Header files for libzbd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libzbd
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libzbd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libzbd.

%package static
Summary:	Static libzbd library
Summary(pl.UTF-8):	Statyczna biblioteka libzbd
License:	LGPL v3+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libzbd library.

%description static -l pl.UTF-8
Statyczna biblioteka libzbd.

%package gui
Summary:	Zoned Block Devices graphical management tools
Summary(pl.UTF-8):	Graficzne narzędzia do zarządzania strefowymi urządzeniami blokowymi
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
Zoned Block Devices graphical management tools.

%description gui -l pl.UTF-8
Graficzne narzędzia do zarządzania strefowymi urządzeniami blokowymi.

%prep
%setup -q

%build
%configure \
	%{!?with_gui:--disable-gui} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libzbd.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/zbd
%attr(755,root,root) %{_libdir}/libzbd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libzbd.so.2
%{_mandir}/man8/zbd.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libzbd.so
%{_includedir}/libzbd
%{_pkgconfigdir}/libzbd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libzbd.a
%endif

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gzbd
%attr(755,root,root) %{_bindir}/gzbd-viewer
%{_datadir}/polkit-1/actions/org.gnome.gzbd-viewer.policy
%{_datadir}/polkit-1/actions/org.gnome.gzbd.policy
%{_desktopdir}/gzbd.desktop
%{_desktopdir}/gzbd-viewer.desktop
%{_pixmapsdir}/gzbd.png
%{_pixmapsdir}/gzbd-viewer.png
%{_mandir}/man8/gzbd.8*
%{_mandir}/man8/gzbd-viewer.8*
%endif
