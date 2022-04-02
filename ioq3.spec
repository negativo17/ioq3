# To avoid shared objects in the data directory, you need to disable shared
# object usage completely that is enabled with the following flags:
#
#   BUILD_GAME_SO=1 (default)
#   BUILD_GAME_QVM=1 (default)
#   COPYDIR=%{buildroot}%{_datadir}/quake3
#   USE_RENDERER_DLOPEN=1 (default)
#   BUILD_RENDERER_OPENGL2=1 (default)
#
# And then you can skip directory creation in the install section and just use
# the "make copyfiles" target."

%global commit0 6d74896557d8c193a9f19bc6845a47e9d0f77db2
%global date 20220321
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           ioq3
Version:        1.36
Release:        41%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Icculus.org Quake III Arena engine
License:        GPLv2+
URL:            http://ioquake3.org/

Source0:        https://github.com/ioquake/%{name}/archive/%{commit0}/%{name}-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

# Generic provider for Quake 3 engine based games
Provides:       quake3-engine = 1.36
# Obsolete official Fedora package
Obsoletes:      ioquake3 < %{version}-%{release}
Provides:       ioquake3 = %{version}-%{release}

BuildRequires:  gcc
BuildRequires:  freetype-devel
BuildRequires:  libXt-devel
BuildRequires:  libcurl-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libvorbis-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  openal-soft-devel
BuildRequires:  opusfile-devel
BuildRequires:  SDL2-devel
BuildRequires:  speex-devel
BuildRequires:  zlib-devel
%ifarch %{ix86} x86_64
BuildRequires:  nasm
%endif

%description
This project, %{name} (or ioq3 for short,) aims to build upon id Software’s
Quake 3 source code release. The source code was released on August 20, 2005
under the GPLv2. Since then, we have been cleaning up, fixing bugs, and adding
features. Our permanent goal is to create the open source Quake 3 distribution
upon which people base their games and projects. We also seek to have the
perfect version of the engine for playing Quake 3: Arena, Team Arena, and all
popular mods. This distribution of the engine has been ported to many new
platforms and has had a slew of new features added, along with massive bug
extermination. While we don’t have PunkBuster (and never will), we do have more
security for servers and clients from various bug fixes which are not in ID’s
client.

%prep
%autosetup -n %{name}-%{commit0}
rm -fr code/{AL,jpeg-8c,libcurl*,libogg*,libspeex*,libvorbis*,SDL2,opus*}

%build
%make_build \
    BUILD_BASEGAME=1 \
    BUILD_CLIENT_SMP=1 \
    BUILD_GAME_SO=0 \
    BUILD_MISSIONPACK=1 \
    BUILD_RENDERER_OPENGL2=0 \
    BUILD_SERVER=1 \
    CFLAGS="%{optflags}" \
    DEFAULT_BASEDIR=%{_datadir}/quake3 \
    USE_CURL=1 \
    USE_CODEC_OPUS=1 \
    USE_CODEC_VORBIS=1 \
    USE_FREETYPE=1 \
    USE_INTERNAL_LIBS=0 \
    USE_OPENAL=1 \
    USE_RENDERER_DLOPEN=0 \
    USE_VOIP=1

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/quake3/baseq3
mkdir -p %{buildroot}%{_datadir}/quake3/missionpack

install -p build/release-linux-*/ioquake3.* %{buildroot}%{_bindir}/ioquake3
install -p build/release-linux-*/ioq3ded.* %{buildroot}%{_bindir}/ioq3ded

%post
/usr/sbin/alternatives --install %{_bindir}/quake3-engine quake3-engine %{_bindir}/ioquake3 10

%preun
if [ "$1" = 0 ]; then
    /usr/sbin/alternatives --remove quake3-engine %{_bindir}/ioquake3
fi

%files
%license COPYING.txt
%doc README.md id-readme.txt md4-readme.txt
%{_bindir}/ioquake3
%{_bindir}/ioq3ded
%{_datadir}/quake3

%changelog
* Sat Apr 02 2022 Simone Caronni <negativo17@gmail.com> - 1.36-41.20220321git6d74896
- Update to latest snapshot.

* Fri Sep 17 2021 Simone Caronni <negativo17@gmail.com> - 1.36-40.20210815git77d6cde
- Update to latest snapshot.

* Wed Apr 07 2021 Simone Caronni <negativo17@gmail.com> - 1.36-39.20210403git4003a5b
- Update to latest snapshot.

* Fri Dec 04 2020 Simone Caronni <negativo17@gmail.com> - 1.36-38.20201117gitd1b7ab6
- Update to latest snapshot.

* Sun Jun 07 2020 Simone Caronni <negativo17@gmail.com> - 1.36-37.20200211gitf2c61c1
- Update to latest snapshot.

* Fri Dec 20 2019 Simone Caronni <negativo17@gmail.com> - 1.36-36.20191207gitdaae32d
- Update to latest snapshot.

* Sun Jan 06 2019 Simone Caronni <negativo17@gmail.com> - 1.36-35.20181222gite5da13f
- Update to latest snapshot.

* Thu May 04 2017 Simone Caronni <negativo17@gmail.com> - 1.36-34.20170428gitc65d2c2
- Update to latest sources.
- Update release to latest packaging guidelines format.

* Mon Jun 13 2016 Simone Caronni <negativo17@gmail.com> - 1.36-33.360ec03
- Update to latest sources.

* Mon Jan 25 2016 Simone Caronni <negativo17@gmail.com> - 1.36-32.558da25
- Update to latest snapshot.
- Update SPEC file to latest packaging guidelines.

* Sat May 02 2015 Simone Caronni <negativo17@gmail.com> - 1.36-1.git.2292bf5
- First build, obsoletes/provides ioquake3.
