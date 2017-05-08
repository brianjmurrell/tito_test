%{?nodejs_find_provides_and_requires}

Name:       device-scanner-daemon
Version:    0.1.0
Release:    1%{?dist}
Summary:    A persistent process that consumes udev events over a unix domain socket.
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/intel-hpdd/device-scanner/tree/master/packages/device-scanner-daemon
Source0:    http://registry.npmjs.org/@mfl/%{name}/-/%{name}-%{version}.tgz

BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

BuildRequires:  nodejs-packaging
Requires: block-device-listener = 0.1.0

%description
A persistent process that consumes udev events over a unix domain socket.
There are two main modes to this daemon:
1. Processing new incoming events. In this mode we will munge and store incoming events.
2. Send current devices object listing. In this mode we will send our current stored devices.
We use unix domain sockets to communicate with the outside world.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/
cp systemd-units/device-scanner.socket $RPM_BUILD_ROOT/usr/lib/systemd/device-scanner.socket
cp systemd-units/device-scanner.service $RPM_BUILD_ROOT/usr/lib/systemd/device-scanner.service
mkdir -p $RPM_BUILD_ROOT/sbin/
cp dist/device-scanner-daemon $RPM_BUILD_ROOT/sbin/device-scanner-daemon

%clean
rm -rf %{buildroot}

%files
%attr(0744,root,root)/sbin/device-scanner-daemon
%attr(0744,root,root)/usr/lib/systemd/device-scanner.service
%attr(0744,root,root)/usr/lib/systemd/device-scanner.socket

%post
systemctl enable device-scanner.socket
systemctl start device-scanner.socket

%preun
systemctl stop device-scanner.socket
systemctl disable device-scanner.socket

%changelog
* Mon May 8 2017 Joe Grund <joe.grund@intel.com> - 0.1.0
- initial package
