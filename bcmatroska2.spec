%global optflags %{optflags} -Wno-incompatible-function-pointer-types

%define major	0
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

%bcond_with	static
%bcond_without	strict

Summary:	Matroska library for mediastreamer
Name:		bcmatroska2
Version:	5.3.36
Release:	1
License:	BSD and Zlib and GPLv2+
Group:		System/Libraries
Url:		https://www.linphone.org
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		bcmatroska2-5.3.5_fix-cmake-dir.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(bctoolbox)

%description
Bcmatroska2 is an implementation of Matroska for mediastreamer.

#---------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Library for accessing USB devices
Group:		System/Libraries

%description -n	%{libname}
Library used by Belledonne Communications
softwares like belle-sip, mediastreamer2 and linphone.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#---------------------------------------------------------------------------

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package includes the development files for %{name}.

%files -n %{devname}
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/
%{_datadir}/cmake/BCMatroska2/

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DCMAKE_SKIP_RPATH:BOOL=YES \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{name} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

