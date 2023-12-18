pkgname = "chromium"
# https://chromiumdash.appspot.com/releases?platform=Linux
pkgver = "120.0.6099.109"
pkgrel = 0
# ppc64le TODO
archs = ["aarch64", "x86_64"]
configure_args = [
    'custom_toolchain="//build/toolchain/linux/unbundle:default"',
    'host_toolchain="//build/toolchain/linux/unbundle:default"',
    'host_pkg_config="/usr/bin/pkg-config"',
    "blink_symbol_level=0",
    "symbol_level=0",
    "chrome_pgo_phase=0",
    'clang_base_path="/usr"',
    "clang_use_chrome_plugins=false",
    'rust_sysroot_absolute="/usr"',
    "treat_warnings_as_errors=false",
    "fatal_linker_warnings=false",
    "disable_fieldtrial_testing_config=true",
    "blink_enable_generated_code_formatting=false",
    "v8_enable_maglev=true",
    "rtc_link_pipewire=true",
    "rtc_use_pipewire=true",
    "link_pulseaudio=true",
    "proprietary_codecs=true",
    "regenerate_x11_protos=true",
    'ffmpeg_branding="Chrome"',
    "icu_use_data_file=false",
    "enable_nacl=false",
    "enable_nocompile_tests_new=false",
    "enable_rust=false",
    "enable_stripping=false",
    "enable_hangout_services_extension=true",
    "enable_vr=false",
    "is_clang=true",
    "is_debug=false",
    "is_official_build=true",
    "is_component_ffmpeg=true",
    "use_custom_libcxx=false",
    "use_gold=false",
    "use_lld=true",
    "use_sysroot=false",
    "use_qt=false",
    "use_pulseaudio=true",
    "use_system_freetype=true",
    "use_system_harfbuzz=true",
    "use_system_lcms2=true",
    "use_system_libdrm=true",
    "use_system_libffi=true",
    "use_system_libjpeg=true",
    "use_system_zlib=true",
]
hostmakedepends = [
    "bash",
    "bison",
    "git",
    "gperf",
    "hwdata",
    # for gn
    "libcxx-devel-static",
    "ninja",
    "nodejs",
    "perl",
    "pkgconf",
    "python",
]
makedepends = [
    "alsa-lib-devel",
    "brotli-devel",
    "bzip2-devel",
    "cairo-devel",
    "clang-devel",
    "cups-devel",
    "dav1d-devel",
    "double-conversion-devel",
    "elfutils-devel",
    "ffmpeg-devel",
    "flac-devel",
    "fontconfig-devel",
    "freetype-devel",
    "glib-devel",
    "gtk+3-devel",
    "heimdal-devel",
    "highway-devel",
    "lcms2-devel",
    "libaom-devel",
    "libavif-devel",
    "libcap-devel",
    "libcurl-devel",
    "libdrm-devel",
    "libevdev-devel",
    "libevent-devel",
    "libexif-devel",
    "libffi-devel",
    "libgcrypt-devel",
    "libjpeg-turbo-devel",
    "libmtp-devel",
    "libpng-devel",
    "libpulse-devel",
    "libsecret-devel",
    "libusb-devel",
    "libva-devel",
    "libxcomposite-devel",
    "libxcursor-devel",
    "libxdamage-devel",
    "libxi-devel",
    "libxml2-devel",
    "libxrandr-devel",
    "libxscrnsaver-devel",
    "libxshmfence-devel",
    "libxslt-devel",
    "libwebp-devel",
    "linux-headers",
    "minizip-devel",
    "musl-bsd-headers",
    "nss-devel",
    "opus-devel",
    "pciutils-devel",
    "pipewire-devel",
    "snappy-devel",
    "speex-devel",
    "sqlite-devel",
    "udev-devel",
    "xcbproto",
    "zlib-devel",
]
depends = [
    "hwdata-usb",
    "xdg-utils",
]
pkgdesc = "Web browser"
maintainer = "q66 <q66@chimera-linux.org>"
license = "BSD-3-Clause"
url = "https://www.chromium.org"
source = f"https://commondatastorage.googleapis.com/chromium-browser-official/chromium-{pkgver}.tar.xz"
sha256 = "87c00c525ee07c2233b78dbece1496b697f686244a67fac2c71e4a30bd96849b"
debug_level = 0
tool_flags = {
    "CFLAGS": [
        "-Wno-unknown-warning-option",
        "-Wno-builtin-macro-redefined",
        "-Wno-deprecated-declarations",
    ],
    "CXXFLAGS": [
        "-Wno-unknown-warning-option",
        "-Wno-builtin-macro-redefined",
        "-Wno-deprecated-declarations",
    ],
}
suid_files = [
    "usr/lib/chromium/chrome-sandbox",
]
hardening = ["!scp"]
# lol
options = ["!cross", "!check"]


def post_patch(self):
    self.mkdir("third_party/node/linux/node-linux-x64/bin", parents=True)
    self.ln_s("/usr/bin/node", "third_party/node/linux/node-linux-x64/bin")

    self.cp(self.files_path / "unbundle.sh", ".")
    self.cp(self.files_path / "pp-data.sh", ".")


def do_configure(self):
    # compile gn early so it can be used to generate gni stuff
    self.do(
        "./tools/gn/bootstrap/bootstrap.py",
        f"-j{self.make_jobs}",
        "--skip-generate-buildfiles",
    )

    _unbundle = [
        "brotli",
        "dav1d",
        "double-conversion",
        "ffmpeg",
        "flac",
        "fontconfig",
        "freetype",
        "harfbuzz-ng",
        "highway",
        "icu",
        "libdrm",
        "libevent",
        "libjpeg",
        "libpng",
        "libsecret",
        "libusb",
        "libwebp",
        "libxml",
        "libxslt",
        "opus",
        "zlib",
        "zstd",
    ]

    for lib in _unbundle:
        self.do("./unbundle.sh", lib)

    self.do("./unbundle.sh", "libjpeg_turbo")

    self.do(
        "./build/linux/unbundle/replace_gn_files.py",
        "--system-libraries",
        *_unbundle,
    )
    self.do("./third_party/libaddressinput/chromium/tools/update-strings.py")

    _confargs = list(self.configure_args)

    _vaapi = "true"
    _cfi = "false"
    _lto = "true" if self.has_lto() else "false"

    match self.profile().arch:
        case "aarch64":
            _confargs.append('target_cpu="arm64"')
            #_cfi = "true"
        case "x86_64":
            _confargs.append('target_cpu="x64"')
            #_cfi = "true"
        case "ppc64le":
            _confargs.append('target_cpu="ppc64"')
            _vaapi = "false"
        case "riscv64":
            _confargs.append('target_cpu="riscv64"')
            _vaapi = "false"

    _confargs += [
        f"use_vaapi={_vaapi}",
        f"is_cfi={_cfi}",
        f"use_thin_lto={_lto}",
    ]

    self.do(
        "./out/Release/gn",
        "gen",
        "out/Release",
        "--args=" + " ".join(_confargs),
    )


def do_build(self):
    self.do(
        "ninja",
        "-C",
        "out/Release",
        f"-j{self.make_jobs}",
        "chrome",
        "chrome_sandbox",
        "chromedriver.unstripped",
        "chrome_crashpad_handler",
        env={"CCACHE_SLOPPINESS": "include_file_mtime"},
    )


def do_install(self):
    srcp = "out/Release"
    dstp = "usr/lib/chromium"

    self.install_license("LICENSE")

    self.install_file(f"{srcp}/chrome", dstp, mode=0o755, name="chromium")
    self.install_file(f"{srcp}/chrome_crashpad_handler", dstp, mode=0o755)
    self.install_file(
        f"{srcp}/chromedriver.unstripped", dstp, mode=0o755, name="chromedriver"
    )
    self.install_file(
        f"{srcp}/chrome_sandbox", dstp, mode=0o4755, name="chrome-sandbox"
    )
    self.install_file(f"{srcp}/libEGL.so", dstp, mode=0o755)
    self.install_file(f"{srcp}/libGLESv2.so", dstp, mode=0o755)
    self.install_file(f"{srcp}/libvulkan.so.1", dstp, mode=0o755)
    self.install_file(f"{srcp}/libvk_swiftshader.so", dstp, mode=0o755)
    self.install_file(f"{srcp}/vk_swiftshader_icd.json", dstp, mode=0o755)
    self.install_file(f"{srcp}/xdg-mime", dstp, mode=0o755)
    self.install_file(f"{srcp}/xdg-settings", dstp, mode=0o755)

    self.install_file(f"{srcp}/*.bin", dstp, glob=True)
    self.install_file(f"{srcp}/*.pak", dstp, glob=True)
    self.install_file(f"{srcp}/locales/*.pak", f"{dstp}/locales", glob=True)

    self.install_files(f"{srcp}/MEIPreload", dstp)

    for s in [24, 48, 64, 128, 256]:
        self.install_file(
            f"chrome/app/theme/chromium/product_logo_{s}.png",
            f"usr/share/icons/hicolor/{s}x{s}/apps",
            name="chromium.png",
        )
    for s in [16, 32]:
        self.install_file(
            f"chrome/app/theme/default_100_percent/chromium/product_logo_{s}.png",
            f"usr/share/icons/hicolor/{s}x{s}/apps",
            name="chromium.png",
        )

    # launcher
    self.install_file(
        self.files_path / "chromium-launcher.sh", dstp, mode=0o755
    )
    self.install_file(self.files_path / "chromium.conf", "etc/chromium")

    self.install_dir("usr/bin")
    self.install_link(
        "../lib/chromium/chromium-launcher.sh", "usr/bin/chromium-browser"
    )
    self.install_link("../lib/chromium/chromedriver", "usr/bin/chromedriver")
    self.install_link("chromium-browser", "usr/bin/chromium")

    # desktop file, manpage etc
    self.do("./pp-data.sh")
    self.install_file("chromium.desktop", "usr/share/applications")
    self.install_file("chromium.appdata.xml", "usr/share/metainfo")
    self.install_man("chromium.1")

    self.error("hi")