# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}


%global blaslib openblas

Name:           eigen3
Version:        3.4.0
Release:        1
Summary:        A lightweight C++ template library for vector and matrix math

License:        MPLv2.0 and LGPLv2+ and BSD
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
Source0:        https://gitlab.com/libeigen/eigen/-/archive/%{version}/eigen-%{version}.tar.bz2
Patch01:        Make_relative_path_variables_of_type_STRING.patch

BuildRequires:  %{blaslib}-devel
BuildRequires:  fftw-devel
BuildRequires:  glew-devel
BuildRequires:  gmp-devel
BuildRequires:  gsl-devel
BuildRequires:  mpfr-devel
BuildRequires:  sparsehash-devel
BuildRequires:  suitesparse-devel
BuildRequires:  gcc-gfortran
BuildRequires:  SuperLU-devel
BuildRequires:  qt-devel
BuildRequires:  scotch-devel
BuildRequires:  metis-devel

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  tex(latex)

%description
%{summary}.


%package devel
Summary:        A lightweight C++ template library for vector and matrix math
BuildArch:      noarch
# -devel subpkg only atm, compat with other distros
Provides:       %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:       %{name}-static = %{version}-%{release}

%description devel
%{summary}.

%package doc
Summary:        Developer documentation for Eigen
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description doc
Developer documentation for Eigen.


%prep
%autosetup -p1 -n eigen-%{version}


%build
mkdir -p build
cd build
%cmake .. \
    -DINCLUDE_INSTALL_DIR=include/%{name} \
    -DBLAS_LIBRARIES="-l%{blaslib}" \
    -DSUPERLU_INCLUDES=%{_includedir}/SuperLU \
    -DSCOTCH_INCLUDES=%{_includedir} -DSCOTCH_LIBRARIES="scotch" \
    -DMETIS_INCLUDES=%{_includedir} -DMETIS_LIBRARIES="metis" \
    -DCMAKEPACKAGE_INSTALL_DIR=share/cmake/%{name}

%make_build all buildtests
%make_build doc

rm -f doc/html/installdox
rm -f doc/html/unsupported/installdox


%install
cd build
%make_install

%check
export EIGEN_SEED=100
export EIGEN_REPEAT=1
ctest -V

%files devel
%license COPYING.README COPYING.BSD COPYING.MPL2 COPYING.LGPL
%{_includedir}/%{name}
%{_datadir}/cmake/%{name}
%{_datadir}/pkgconfig/%{name}.pc

%files doc
%doc build/doc/html


%changelog
* Wed Jun 15 2022 lvxiaoqian <xiaoqian@nj.iscas.ac.cn> - 3.4.0-1
- Initial package
