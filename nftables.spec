%define rpmversion 0.8
%define specrelease 7%{?dist}
%define libnftnlversion 1.0.8-1

Name:           nftables
Version:        %{rpmversion}
Release:        %{specrelease}
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
BuildRequires:  libnftnl-devel >= %{libnftnlversion}
# docbook2X is available in EPEL repo only, which is not included in Brew
#BuildRequires:  docbook2X
#BuildRequires:  docbook-dtds
BuildRequires:  systemd
Patch0:             0001-src-fix-protocol-context-update-on-big-endian-system.patch
Patch1:             0002-netlink_linearize-exthdr-op-must-be-u32.patch

%description
Netfilter Tables userspace utilities.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules DOCBOOK2X_MAN="no" DOCBOOK2MAN="no" DB2X_DOCBOOK2MAN="no"
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
for f in $RPM_BUILD_ROOT/%{_sysconfdir}/nftables/*; do
	echo "# include \"%{_sysconfdir}/nftables/$(basename $f)\""
done >> $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/nftables.conf
chmod 600 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/nftables.conf
chmod 750 $RPM_BUILD_ROOT/%{_sysconfdir}/nftables/
chmod 600 $RPM_BUILD_ROOT/%{_sysconfdir}/nftables/*

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
* Mon Dec 18 2017 Phil Sutter <psutter@redhat.com> [0.8-7.el7]
- A proper fix for incompatible docbook2man (Phil Sutter) [1523239]

* Thu Dec 14 2017 Phil Sutter <psutter@redhat.com> [0.8-6.el7]
- netlink_linearize: exthdr op must be u32 (Phil Sutter) [1524246]
- src: fix protocol context update on big-endian systems (Phil Sutter) [1523016]

* Fri Dec 08 2017 Phil Sutter <psutter@redhat.com> [0.8-5.el7]
- Prevent build failure due to incompatible docbook2man (Phil Sutter) [1523239]

* Sat Oct 14 2017 Phil Sutter <psutter@redhat.com> [0.8-4.el7]
- Update /etc/sysconfig/nftables.conf with new config samples (Phil Sutter) [1472261]

* Fri Oct 13 2017 Phil Sutter <psutter@redhat.com> [0.8-3.el7]
- Fix typo in spec file (Phil Sutter) [1451404]

* Fri Oct 13 2017 Phil Sutter <psutter@redhat.com> [0.8-2.el7]
- Fix permissions of installed config files (Phil Sutter) [1451404]

* Fri Oct 13 2017 Phil Sutter <psutter@redhat.com> [0.8-1.el7]
- Rebase onto upstream version 0.8 (Phil Sutter) [1472261]

* Fri May 12 2017 Phil Sutter <psutter@redhat.com> [0.6-4.el7]
- evaluate: Avoid undefined behaviour in concat_subtype_id() (Phil Sutter) [1360789]
- src: Interpret OP_NEQ against a set as OP_LOOKUP (Phil Sutter) [1440011]
- include: refresh uapi/linux/netfilter/nf_tables.h copy (Phil Sutter) [1440011]
- datatype: time_type should send milliseconds to userspace (Phil Sutter) [1427114]
- meta: fix memory leak in tc classid parser (Phil Sutter) [1380326]
- src: meta priority support using tc classid (Phil Sutter) [1380326]
- src: simplify classid printing using x instead of 04x (Phil Sutter) [1380326]
- src: rename datatype name from tc_handle to classid (Phil Sutter) [1380326]
- payload: don't update protocol context if we can't find a description (Timothy Redaelli) [1446534 1399764]
- evaluate: reject: Have a generic fix for missing network context (Timothy Redaelli) [1360354]

* Mon Mar 06 2017 Phil Sutter <psutter@redhat.com> [0.6-3.el7]
- nftables.spec: Require at least libnftnl-1.0.6-4 (Phil Sutter) [1358705]
- evaluate: Fix datalen checks in expr_evaluate_string() (Phil Sutter) [1360240]
- netlink_delinearize: Avoid potential null pointer deref (Timothy Redaelli) [1360257]
- src: use new range expression for != [a,b] intervals (Phil Sutter) [1358705]

* Tue Jul 19 2016 Phil Sutter <psutter@redhat.com> 0.6-2
- Add pre-generated nft.8 to overcome missing docbook2X package.

* Wed Jun 29 2016 Phil Sutter <psutter@redhat.com> 0.6-1
- Rebased from Fedora Rawhide and adjusted for RHEL review.
