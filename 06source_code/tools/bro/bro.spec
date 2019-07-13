

# Conditionals
%bcond_without kafka


Name:           bro
Version:        %{release_version}
Release:        %{release_num}%{dist}
Summary:        Bro is a powerful framework for network analysis and security monitoring
Group:          Productivity/Networking/Diagnostic

License:        BSD-3-Clause
URL:            http://bro.org
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  flex bison cmake openssl-devel zlib-devel python-devel swig gcc-c++
BuildRequires:  libpcap-devel
Requires(pre):  /usr/sbin/groupadd, /usr/bin/getent

%if %{defined rhel_version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%define _prefix     /opt/%{name}-%{version}


%if 0%{?suse_version}
%define __cmake /usr/bin/cmake
%endif

%description
Bro is a powerful network analysis framework.


%pre
/usr/bin/getent group bro >/dev/null || /usr/sbin/groupadd -r bro


%prep
%setup -n bro-%{version} -q


%build
./configure --prefix=%{_prefix} --binary-package 
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

%if %{defined rhel_version}
make install DESTDIR=$RPM_BUILD_ROOT

%else
%make_install

%endif


%post
ln -sf %{_prefix} /opt/%{name}

%postun 
rm -rf %{_prefix}
rm -rf /opt/%{name}

%files
%defattr(-,root,root,-)
%{_prefix}/*


%doc CHANGES COPYING NEWS README VERSION


