Summary:	Security auditing on UNIX systems
Name:		tiger
Version:	3.2.2
Release:	0.1
License:	GPL+
Group:		Applications/System
Source0:	http://savannah.nongnu.org/download/tiger/%{name}-%{version}.tar.gz
# Source0-md5:	00e85a371989a533164beaea8ed5af01
URL:		http://www.nongnu.org/tiger/
Source2:	%{name}.cron
Source3:	%{name}.ignore
Source4:	%{name}.ignore.server
BuildRequires:	autoconf
BuildRequires:	recode
Requires:	bash
Requires:	crondaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	no_install_post_check_tmpfiles 1

%description
TIGER, or the "tiger" scripts, is a set of Bourne shell scripts, C
programs and data files which are used to perform a security audit of
UNIX systems. It is designed to hopefully be easy to use, easy to
understand and easy to enhance.

%prep
%setup -q

find -name "*.rpmorig" -o -name "*.orig" -o -name "*.old" -delete

recode ISO-8859-1..UTF-8 man/tiger.8.in

install -d examples
cp -p cronrc tigerrc tigerrc-all tigerrc-dist tigerrc-TAMU \
      site-sample site-saturn %{SOURCE4} examples

%build
autoreconf -i
%configure \
	--with-tigerhome=%{_libdir}/%{name} \
	--with-tigerwork=%{_localstatedir}/run/tiger/work \
	--with-tigerlog=%{_localstatedir}/log/tiger \
	--with-tigerbin=%{_sbindir} \
	--with-tigerconfig=%{_sysconfdir}/tiger

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.d,%{_sysconfdir}/%{name}/templates}
%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/tiger
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tiger.ignore
cp -p version.h $RPM_BUILD_ROOT%{_libdir}/%{name}

ln -s %{_sbindir}/tigexp $RPM_BUILD_ROOT%{_libdir}/%{name}/tigexp

# Perm fixes
chmod +x $RPM_BUILD_ROOT%{_libdir}/%{name}/systems/Linux/2/check_*

# Unwanted OS
rm -r $RPM_BUILD_ROOT%{_libdir}/%{name}/systems/{AIX,HPUX,IRIX,NeXT,SunOS,UNICOS,UNICOSMK,Tru64,MacOSX}
# Documentation (in %doc)
rm -r $RPM_BUILD_ROOT%{_libdir}/%{name}/html
rm -r $RPM_BUILD_ROOT%{_libdir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc USING BUGS.EXTERN DESCRIPTION CREDITS README README.1st README.hostids
%doc README.ignore README.linux README.signatures README.sources
%doc README.time README.unsupported README.writemodules TODO
%doc examples html
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/cronrc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/tiger.ignore
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/tigerrc
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/tiger
%attr(755,root,root) %{_sbindir}/tiger
%attr(755,root,root) %{_sbindir}/tigercron
%attr(755,root,root) %{_sbindir}/tigexp
%{_mandir}/man8/tiger.8*
%{_mandir}/man8/tigercron.8*
%{_mandir}/man8/tigexp.8*
%dir %{_localstatedir}/run/tiger
%dir %{_localstatedir}/log/tiger

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/version.h
%dir %{_libdir}/%{name}/bin
%attr(755,root,root) %{_libdir}/%{name}/bin/*
%{_libdir}/%{name}/config
%{_libdir}/%{name}/initdefs
%{_libdir}/%{name}/syslist
%{_libdir}/%{name}/systems
%{_libdir}/%{name}/tigexp

%dir %{_libdir}/%{name}/scripts
%attr(755,root,root) %{_libdir}/%{name}/scripts/*_run
%attr(755,root,root) %{_libdir}/%{name}/scripts/check_*
%attr(755,root,root) %{_libdir}/%{name}/scripts/find_files
%dir %{_libdir}/%{name}/scripts/sub
%attr(755,root,root) %{_libdir}/%{name}/scripts/sub/check_*

%dir %{_libdir}/%{name}/util
%attr(755,root,root) %{_libdir}/%{name}/util/*

%dir %{_libdir}/%{name}/check.d
%{_libdir}/%{name}/check.d/README
