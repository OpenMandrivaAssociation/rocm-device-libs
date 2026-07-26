# Bitcode has no useful debuginfo
%global debug_package %{nil}

Name:		rocm-device-libs
Version:	7.14.0
Release:	1
%{!?rocm_llvm_maj_ver:%global rocm_llvm_maj_ver 23}
Summary:	AMD ROCm device-side LLVM bitcode libraries
License:	NCSA
Group:		System/Libraries
URL:		https://github.com/ROCm/llvm-project
# Filtered sources: amd/device-libs from llvm-project @ therock-7.14
Source0:	rocm-device-libs-%{version}.tar.gz
Patch0:		clang23-attribute-alias.patch

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	lib64clang-devel >= %{rocm_llvm_maj_ver}
BuildRequires:	lib64llvm-devel >= %{rocm_llvm_maj_ver}
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(libzstd)

Requires:	clang >= %{rocm_llvm_maj_ver}

ExclusiveArch:	%{x86_64} %{aarch64}

%description
AMD-specific device-side language runtime libraries as LLVM bitcode
(ocml, ockl, opencl, hip, oclc controls, asanrtl, …). Built entirely from
source on ABF from the TheRock 7.14 device-libs tree.

%prep
%autosetup -n rocm-device-libs-%{version} -p1

# Configure in %%prep so %%build starts from the source root again
# (%%cmake leaves the shell in the build/ directory).
# gfx9-generic: system clang 23 needs a baseline ISA so feature-gated
# amdgcn builtins (msad, …) are available when emitting bitcode.
# ROCM_DEVICE_LIBS_BITCODE_INSTALL_LOC_NEW places bitcode under
# %%{_libdir}/amdgcn/bitcode (FHS; not /usr/amdgcn).
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DCLANG_OPTIONS_APPEND=-mcpu=gfx9-generic \
	-DROCM_DEVICE_LIBS_BITCODE_INSTALL_LOC_NEW=%{_lib}/amdgcn \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%license LICENSE.TXT
%doc README.md
%exclude %{_docdir}/rocm-device-libs/LICENSE.TXT
%{_libdir}/cmake/AMDDeviceLibs
%dir %{_libdir}/amdgcn
%dir %{_libdir}/amdgcn/bitcode
%{_libdir}/amdgcn/bitcode/*.bc
