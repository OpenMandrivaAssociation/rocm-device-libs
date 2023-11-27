# bitcode has no debuginfo
%global debug_package %{nil}
 
%global llvm_maj_ver 17
# If you bump LLVM, please reset bugfix_version to 0; I fork upstream sources,
# but I prepare the initial *.0 tag long before Fedora/EL picks up new LLVM.
# An LLVM update will require uploading new sources, contact mystro256 if FTBFS.
%global bugfix_version 1
%global upstreamname ROCm-Device-Libs-rocm
 
 
Name:           rocm-device-libs
Version:        5.7.1
Release:        1
Summary:        AMD ROCm LLVM bit code libraries
 
Url:            https://github.com/RadeonOpenCompute/ROCm-Device-Libs
License:        NCSA
# Use fork upstream sources because they don't target stable LLVM, but rather the
# bleeding edge LLVM branch. This fork is a snapshot with bugfixes backported:
Source0:        https://github.com/mystro256/%{upstreamname}/archive/refs/tags/%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  clang-devel
BuildRequires:  clang
BuildRequires:  llvm-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(libzstd)
Requires:       clang
 
%description
This package contains a set of AMD specific device-side language runtime
libraries in the form of bit code. Specifically:
 - Open Compute library controls
 - Open Compute Math library
 - Open Compute Kernel library
 - OpenCL built-in library
 - HIP built-in library
 - Heterogeneous Compute built-in library
 
%prep
%autosetup -n %{upstreamname}-%{version} -p1
 
%build
%cmake -DCMAKE_BUILD_TYPE="RELEASE"
%make_build

%install
%make_install -C build

%files
%license LICENSE.TXT
%doc README.md doc/*.md
# No need to install this twice:
%exclude %{_docdir}/ROCm-Device-Libs/LICENSE.TXT
%{_libdir}/cmake/AMDDeviceLibs
%clang_resource_dir/amdgcn
