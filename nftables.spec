%define rpmversion 0.6
%define specrelease 4%{?dist}
%define libnftnlversion 1.0.6-4

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
Patch0:             0001-src-use-new-range-expression-for-a-b-intervals.patch
Patch1:             0002-netlink_delinearize-Avoid-potential-null-pointer-der.patch
Patch2:             0003-evaluate-Fix-datalen-checks-in-expr_evaluate_string.patch
Patch3:             0004-evaluate-reject-Have-a-generic-fix-for-missing-netwo.patch
Patch4:             0005-payload-don-t-update-protocol-context-if-we-can-t-fi.patch
Patch5:             0006-src-rename-datatype-name-from-tc_handle-to-classid.patch
Patch6:             0007-src-simplify-classid-printing-using-x-instead-of-04x.patch
Patch7:             0008-src-meta-priority-support-using-tc-classid.patch
Patch8:             0009-meta-fix-memory-leak-in-tc-classid-parser.patch
Patch9:             0010-datatype-time_type-should-send-milliseconds-to-users.patch
Patch10:            0011-include-refresh-uapi-linux-netfilter-nf_tables.h-cop.patch
Patch11:            0012-src-Interpret-OP_NEQ-against-a-set-as-OP_LOOKUP.patch
Patch12:            0013-evaluate-Avoid-undefined-behaviour-in-concat_subtype.patch

%description
Netfilter Tables userspace utilities.

%prep
%autosetup -p1

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
