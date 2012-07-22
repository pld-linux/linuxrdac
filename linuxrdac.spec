#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)

%define		rel	12
%define		pname	linuxrdac
Summary:	RDAC Multi-Path Proxy Driver for Linux
Name:		%{pname}%{_alt_kernel}
Version:	09.03.0C06.0452.2
Release:	%{rel}
License:	GPLv2
Group:		Base/Kernel
Source0:	linuxrdac-%{version}-mktarball.dkms.tgz
# Source0-md5:	da1dadb0d8ac09661bb407386a212a82
Patch0:		linuxrdac-linux-2.6.39.patch
Patch1:		linuxrdac-linux-3.4.patch
#URL:		-
BuildRequires:	rpmbuild(macros) >= 1.379
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RDAC Multi-Path Proxy Driver for Linux.

%package -n kernel%{_alt_kernel}-scsi-mpprdac
Summary:	RDAC Multi-Path Proxy Driver for Linux
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-scsi-mpprdac
RDAC Multi-Path Proxy Driver for Linux.

%prep
%setup -q -c
mv dkms_source_tree/* .
%patch0 -p1
%patch1 -p2

%build
%{__make} -j1 \
	KERNEL_OBJ=%{_kernelsrcdir}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m mppVhba,mppUpper -d kernel/drivers/scsi

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-scsi-mpprdac
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-scsi-mpprdac
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-scsi-mpprdac
%defattr(644,root,root,755)
%doc Readme.txt
/lib/modules/%{_kernel_ver}/kernel/drivers/scsi/*.ko*
