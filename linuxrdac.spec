#
# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	65
%define		pname	linuxrdac
Summary:	RDAC Multi-Path Proxy Driver for Linux
Name:		%{pname}%{_alt_kernel}
Version:	09.03.0C06.0452.2
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPLv2
Group:		Base/Kernel
Source0:	linuxrdac-%{version}-mktarball.dkms.tgz
# Source0-md5:	da1dadb0d8ac09661bb407386a212a82
Patch0:		linuxrdac-linux-2.6.39.patch
Patch1:		linuxrdac-linux-3.4.patch
Patch2:		linuxrdac-linux-3.7.patch
#URL:		-
BuildRequires:	rpmbuild(macros) >= 1.678
%{expand:%kbrs}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RDAC Multi-Path Proxy Driver for Linux.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-scsi-mpprdac\
Summary:	RDAC Multi-Path Proxy Driver for Linux\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-scsi-mpprdac\
RDAC Multi-Path Proxy Driver for Linux.\
\
%files -n kernel%{_alt_kernel}-scsi-mpprdac\
%defattr(644,root,root,755)\
%doc Readme.txt\
/lib/modules/%{_kernel_ver}/kernel/drivers/scsi/*.ko*\
\
%post -n kernel%{_alt_kernel}-scsi-mpprdac\
%depmod %{_kernel_ver}\
\
%postun -n kernel%{_alt_kernel}-scsi-mpprdac\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%{__make} -j1 KERNEL_OBJ=%{_kernelsrcdir} clean\
%{__make} -j1 KERNEL_OBJ=%{_kernelsrcdir}\
%install_kernel_modules -D installed -m mppVhba,mppUpper -d kernel/drivers/scsi\
%{nil}

%{expand:%kpkg}

%prep
%setup -q -c
mv dkms_source_tree/* .
%patch0 -p1
%patch1 -p2
%patch2 -p1

%build
%{expand:%bkpkg}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
