Name:           nftables
Version:        0.6
Release:        2%{?dist}
Summary:        Netfilter Tables userspace utillites
License:        GPLv2
URL:            http://netfilter.org/projects/nftables/
Source0:        http://ftp.netfilter.org/pub/nftables/nftables-%{version}.tar.bz2
Source1:        nftables.service
Source2:        nftables.conf
Source3:        nft.8
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  libmnl-devel
BuildRequires:  gmp-devel
BuildRequires:  readline-devel
BuildRequires:  libnftnl-devel
# docbook2X is available in EPEL repo only, which is not included in Brew
#BuildRequires:  docbook2X
#BuildRequires:  docbook-dtds
BuildRequires:  systemd

%description
Netfilter Tables userspace utilities.

%prep
%setup -q

%build
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
cp -a %{SOURCE3} $RPM_BUILD_ROOT/%{_mandir}/man8/
chmod 644 $RPM_BUILD_ROOT/%{_mandir}/man8/nft*

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
cp -a %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
cp -a %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/

%post
%systemd_post nftables.service

%preun
%systemd_preun nftables.service

%postun
%systemd_postun_with_restart nftables.service

%files
%doc COPYING TODO
%config(noreplace) %{_sysconfdir}/nftables/
%config(noreplace) %{_sysconfdir}/sysconfig/nftables.conf
%{_sbindir}/nft
%{_mandir}/man8/nft*
%{_unitdir}/nftables.service

%changelog
* Tue Jul 19 2016 Phil Sutter <psutter@redhat.com> 0.6-2
- Add pre-generated nft.8 to overcome missing docbook2X package.

* Wed Jun 29 2016 Phil Sutter <psutter@redhat.com> 0.6-1
- Rebased from Fedora Rawhide and adjusted for RHEL review.
