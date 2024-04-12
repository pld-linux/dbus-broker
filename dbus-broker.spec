Summary:	Linux D-Bus Message Broker
Name:		dbus-broker
Version:	36
Release:	0.1
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/bus1/dbus-broker/releases/download/v%{version}/dbus-broker-%{version}.tar.xz
# Source0-md5:	0398b41a250a6172e35750fc864ee33b
URL:		https://github.com/bus1/dbus-broker/wiki
BuildRequires:	audit-libs-devel >= 3.0
BuildRequires:	c-dvar-devel >= 1.1.0
BuildRequires:	c-ini-devel >= 1.1.0
BuildRequires:	c-list-devel >= 3.1.0
BuildRequires:	c-rbtree-devel >= 3.2.0
BuildRequires:	c-shquote-devel >= 1.1.0
BuildRequires:	c-stdaux-devel >= 1.5.0
BuildRequires:	docutils
BuildRequires:	expat-devel >= 2.2
BuildRequires:	libapparmor-devel >= 3.0
BuildRequires:	libcap-ng-devel >= 0.6
BuildRequires:	libselinux-devel >= 3.2
BuildRequires:	linux-libc-headers >= 7:4.17
BuildRequires:	meson >= 0.60.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-devel >= 1:230
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	audit-libs >= 3.0
Requires:	c-dvar >= 1.1.0
Requires:	c-ini >= 1.1.0
Requires:	c-rbtree >= 3.2.0
Requires:	c-shquote >= 1.1.0
Requires:	expat >= 2.2
Requires:	libapparmor >= 3.0
Requires:	libcap-ng >= 0.6
Requires:	libselinux >= 3.2
Requires:	uname(release) >= 4.17
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The dbus-broker project is an implementation of a message bus as
defined by the D-Bus specification. Its aim is to provide high
performance and reliability, while keeping compatibility to the D-Bus
reference implementation. It is exclusively written for linux systems,
and makes use of many modern features provided by recent linux kernel
releases.

%prep
%setup -q

%build
%meson build \
	-Dapparmor=true \
	-Daudit=true \
	-Dlinux-4-17=true \
	-Dselinux=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post dbus-broker.service
%systemd_user_post dbus-broker.service

%preun
%systemd_preun dbus-broker.service
%systemd_user_preun dbus-broker.service

%postun
%systemd_postun dbus-broker.service
%systemd_user_postun dbus-broker.service

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-broker
%attr(755,root,root) %{_bindir}/dbus-broker-launch
%{systemdunitdir}/dbus-broker.service
%{systemduserunitdir}/dbus-broker.service
%{_prefix}/lib/systemd/catalog/dbus-broker.catalog
%{_prefix}/lib/systemd/catalog/dbus-broker-launch.catalog
