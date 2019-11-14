Name:    wiremock
Version: 2.25.1
Release: 1
Summary: RPM for tool for mocking HTTP services

Group:   Development Tools
License: ASL 2.0
URL: http://repo1.maven.org/maven2/com/github/tomakehurst/wiremock-standalone/%{version}/wiremock-standalone-%{version}.jar
Source0: %{name}.service
Source1: 204.json
Source2: 301.json
Source3: 302.json
Source4: 304.json
Source5: 400.json
Source6: 401.json
Source7: 403.json
Source8: 404.json
Source9: 405.json
Source10: 408.json
Source11: 500.json
Source12: 502.json
Source13: 503.json
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel
BuildRequires: tree

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%if %use_systemd
BuildRequires: systemd
%endif

%description
WireMock is a simulator for HTTP-based APIs.
Some might consider it a service virtualization tool or a mock server.

%prep
curl -L %{url} > wiremock.jar

%install
ls
pwd
tree
%{__install} -m 0755 -d %{buildroot}/usr/lib/%{name}/%{name}
%{__install} -m 0755 %{SOURCE0} %{buildroot}/usr/lib/%{name}/%{name}
%{__install} -m 0755 -d %{buildroot}/usr/lib/%{name}/mappings
cp %{SOURCE1} %{buildroot}/usr/lib/%{name}/mappings
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} \
    %{buildroot}%{_unitdir}/%{name}.service
%endif

%pre
/usr/bin/getent group wiremock > /dev/null || /usr/sbin/groupadd -r wiremock
/usr/bin/getent passwd wiremock > /dev/null || /usr/sbin/useradd -r -d /usr/lib/%{name} -s /bin/bash -g wiremock wiremock

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop %{name}
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%files
/usr/lib/%{name}/%{name}
/usr/lib/%{name}/mappings/503.json
%dir %attr(0775, wiremock, wiremock) /usr/lib/%{name}/%{name}
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif
