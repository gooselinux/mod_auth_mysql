Summary: Basic authentication for the Apache web server using a MySQL database
Name: mod_auth_mysql
Version: 3.0.0
Release: 11%{?dist}.1
Epoch: 1
Group: System Environment/Daemons
URL: http://modauthmysql.sourceforge.net/
Source0: http://downloads.sourceforge.net/modauthmysql/mod_auth_mysql-%{version}.tar.gz
Source1: auth_mysql.conf
Patch0: mod_auth_mysql-3.0.0-apr1x.patch
Patch1: mod_auth_mysql-3.0.0-disable.patch
Patch10: mod_auth_mysql-3.0.0-CVE-2008-2384.patch
License: ASL 1.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: httpd-devel, mysql-devel
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo missing httpd-devel)

%description
mod_auth_mysql can be used to limit access to documents served by a
web server by checking data in a MySQL database.

%prep
%setup -q
%patch0 -p1 -b .apr1x
%patch1 -p1 -b .disable

%patch10 -p1 -b .cve2384

%build
%{_sbindir}/apxs -I%{_includedir}/mysql -Wc,-Wall -Wc,-Werror \
        -c %{name}.c -L%{_libdir}/mysql -lmysqlclient

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m755 .libs/%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# Install the config file
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/

# Extract the license
sed -n '0,/\*\//p' mod_auth_mysql.c > LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README CONFIGURE CHANGES LICENSE
%{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Thu Dec 16 2010 Joe Orton <jorton@redhat.com> - 1:3.0.0-11.1
- add security fix for CVE-2008-2384 (#663617)

* Sat Jun 19 2010 Joe Orton <jorton@redhat.com> - 1:3.0.0-11
- less noise for httpd-mmn BR; package the LICENSE (#605950)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:3.0.0-10.1
- Rebuilt for RHEL 6

* Fri Aug 07 2009 Parag <paragn@fedoraproject.org> 1:3.0.0-10
- Spec cleanup as suggested in review bug #226152

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Joe Orton <jorton@redhat.com> 1:3.0.0-7
- rebuild for new MySQL

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.0.0-6
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 1:3.0.0-5
- fix License

* Wed Jun 20 2007 Joe Orton <jorton@redhat.com> 1:3.0.0-4
- tweak %%summary, use standard BuildRoot

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.0-3.1
- rebuild

* Tue Feb 28 2006 Joe Orton <jorton@redhat.com> 1:3.0.0-3
- fix to disable auth by default again (regression since FC4)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.0-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.0.0-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Joe Orton <jorton@redhat.com> 1:3.0.0-2
- update to 3.0.0

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 1:2.9.0-2
- Rebuild due to mysql update.

* Thu Jun 16 2005 Joe Orton <jorton@redhat.com> 1:2.9.0-1
- update to 2.9.0 (#160239)

* Thu Mar  3 2005 Joe Orton <jorton@redhat.com> 1:2.6.1-4
- pass -Wall/-Werror to apxs via -Wc,

* Mon Jan 31 2005 Joe Orton <jorton@redhat.com> 1:2.6.1-3.1
- really remove RPATH; build against MySQL 4.x

* Wed Nov 24 2004 Joe Orton <jorton@redhat.com> - 1:2.6.1-2.1
- rebuild

* Mon Nov  1 2004 Joe Orton <jorton@redhat.com> 1:2.6.1-2
- remove RPATH

* Fri Oct 29 2004 Joe Orton <jorton@redhat.com> 2.6.1-1
- update to 2.6.1
- rebuild against mysqlclient10-devel
- don't strip the module in %%build

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 20030510-3
- rebuild for old MySQL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 20030510-2
- rebuilt

* Tue May 13 2003 Gary Benson <gbenson@redhat.com> 20030510-1
- upgrade to 20030510

* Tue May 13 2003 Joe Orton <jorton@redhat.com> 1.11-13
- rebuild for httpd-2.0.45

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.11-12
- rebuilt

* Wed Nov  6 2002 Joe Orton <jorton@redhat.com> 1.11-11
- rebuild in new environment

* Mon Sep  2 2002 Joe Orton <jorton@redhat.com> 1.11-10
- require httpd-mmn for module ABI compatibility

* Fri Aug 29 2002 Gary Benson <gbenson@redhat.com> 1.11-9
- tweak examples in auth_mysql.conf to use fewer MySQLisms and to
  neither assume the existence of nor trample all over the 'test'
  database.

* Thu Aug 29 2002 Gary Benson <gbenson@redhat.com> 1.11-8
- add some examples to /etc/httpd/conf.d/auth_mysql.conf (#71317)

* Mon Aug 12 2002 Gary Benson <gbenson@redhat.com> 1.11-7
- rebuild against httpd-2.0.40

* Fri Jun 21 2002 Gary Benson <gbenson@redhat.com> 1.11-6
- move /etc/httpd2 back to /etc/httpd

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.11-5
- automated rebuild

* Thu May 30 2002 Gary Benson <gbenson@redhat.com> 1.11-4
- port to httpd-2.0
- add the config file
- tidy up the extracted readme

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 1.11-3
- rebuild in new environment

* Wed Sep  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.11 from 30 August, fixing problems detailed at
  http://cert.uni-stuttgart.de/advisories/apache_auth.php

* Fri May 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
