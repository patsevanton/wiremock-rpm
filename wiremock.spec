Name:    wiremock
Version: 2.25.1
Release: 16
Summary: Tool for mocking HTTP services

Group:   Development Tools
License: ASL 2.0
URL: http://repo1.maven.org/maven2/com/github/tomakehurst/wiremock-standalone/%{version}/wiremock-standalone-%{version}.jar
Source0: wiremock.service
Source1: 102.json
Source2: 204.json
Source3: 301.json
Source4: 302.json
Source5: 304.json
Source6: 400.json
Source7: 401.json
Source8: 403.json
Source9: 404.json
Source10: 405.json
Source11: 408.json
Source12: 500.json
Source13: 502.json
Source14: 503.json
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel
Requires: java-openjdk

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%if %use_systemd
BuildRequires: systemd
%endif

%description
WireMock is a simulator for HTTP-based APIs.
Some might consider it a service virtualization tool or a mock server.

%package popular-json
Summary: Popular JSON for WireMock.

%description popular-json
Popular JSON for WireMock.

%prep
curl -L %{url} > wiremock.jar

%install
%{__install} -m 0755 -d %{buildroot}/usr/lib/wiremock
cp wiremock.jar %{buildroot}/usr/lib/wiremock/wiremock.jar
%{__install} -m 0755 -d %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE1} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE2} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE3} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE4} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE5} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE6} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE7} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE8} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE9} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE10} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE11} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE12} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE13} %{buildroot}/usr/lib/wiremock/mappings
cp %{SOURCE14} %{buildroot}/usr/lib/wiremock/mappings
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} \
    %{buildroot}%{_unitdir}/wiremock.service
%endif

%pre
/usr/bin/getent group wiremock > /dev/null || /usr/sbin/groupadd -r wiremock
/usr/bin/getent passwd wiremock > /dev/null || /usr/sbin/useradd -r -d /usr/lib/wiremock -s /bin/bash -g wiremock wiremock

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop wiremock
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%files
%dir %attr(0775, wiremock, wiremock) /usr/lib/wiremock
/usr/lib/wiremock/wiremock.jar
%if %{use_systemd}
%{_unitdir}/wiremock.service
%endif

%files popular-json
%defattr(-,wiremock,wiremock)
/usr/lib/wiremock/mappings/*
