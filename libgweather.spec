Summary:	Library to access weather information from online services for numerous locations
Name:		libgweather
Version:	3.12.0
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libgweather/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	5bba1f4fcfcd175e34859b6cfbc51637
Patch0:		%{name}-Landshut.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	intltool
BuildRequires:	libsoup-gnome-devel >= 2.46.0
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgweather is a library to access weather information from online
services for numerous locations.

%package devel
Summary:	Header files for libgweather
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libgweather.

%package data
Summary:	libgweather data
Group:		X11/Development/Libraries
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name} = %{version}-%{release}

%description data
libgweather data.

%package apidocs
Summary:	libgweather API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libgweather API documentation.

%prep
%setup -q
%patch0 -p1

# https://bugzilla.gnome.org/show_bug.cgi?id=614645
%{__sed} -i -e 's|gnome|hicolor|g' icons/Makefile.am

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}	\
	--with-zoneinfo-dir=%{_datadir}/zoneinfo
%{__make}
%{__make} check

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,es_*}
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang libgweather-3.0 --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post data
%update_icon_cache hicolor
%update_gsettings_cache

%postun data
%update_icon_cache hicolor
%update_gsettings_cache

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %ghost %{_libdir}/libgweather-3.so.?
%attr(755,root,root) %{_libdir}/libgweather-3.so.*.*.*
%{_libdir}/girepository-1.0/GWeather-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgweather-3.so
%{_includedir}/libgweather-3.0
%{_pkgconfigdir}/gweather-3.0.pc
%{_datadir}/gir-1.0/GWeather-3.0.gir
%{_datadir}/vala/vapi/gweather-3.0.vapi

%files data -f libgweather-3.0.lang
%defattr(644,root,root,755)
%dir %{_datadir}/libgweather
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.GWeather.gschema.xml
%{_datadir}/libgweather/Locations.xml
%{_datadir}/libgweather/locations.dtd
%{_iconsdir}/hicolor/*/status/*.png

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}-3.0

