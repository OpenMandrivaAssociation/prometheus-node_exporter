%define debug_package %{nil}

%global provider	github
%global provider_tld	com
%global project		prometheus
%global repo		node_exporter
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

%global build_tag	v%{version}

Summary:	Prometheus exporter for machine metrics
Name:		prometheus-%{repo}
Version:	0.18.1
Release:	1
License:	Apache 2.0
Url:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/v%{version}.tar.gz
Source1:	prometheus-node_exporter.service
Source2:	node_exporter.sysconfig
BuildRequires:	golang
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
Prometheus exporter for machine metrics, written in Go with pluggable
metric collectors.

%prep
%setup -q -n %{repo}-%{version}
rm -f go.mod

%build
export GOPATH=$(pwd):%{gopath}
mkdir -p src/github.com/prometheus
ln -s ../../../ src/github.com/prometheus/node_exporter

%gobuild -o bin/node_exporter %{import_path}

%install
install -m755 -D bin/%{repo} %{buildroot}%{_bindir}/prometheus-%{repo}
install -m644 -D %{SOURCE1} %{buildroot}%{_unitdir}/prometheus-node_exporter.service
install -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/prometheus-node_exporter

%post
%systemd_post %{repo}.service

%preun
%systemd_preun %{repo}.service

%postun
%systemd_postun_with_restart %{repo}.service

%files
%config(noreplace) %{_sysconfdir}/sysconfig/prometheus-node_exporter
%{_bindir}/prometheus-node_exporter
%{_unitdir}/prometheus-node_exporter.service
