from conan import ConanFile
import os
import subprocess

class libxkbcommon(ConanFile):
    name = "libxkbcommon"
    version = "master"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "wayland/[>=1.24]",
        "wayland-protocols/[>=1.4]",
    )

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:xkbcommon/libxkbcommon.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        meson_native = self.conf.get("user.mccakit:meson_native", None)
        meson_cross = self.conf.get("user.mccakit:meson_cross", None)

        os.chdir("libxkbcommon")
        pkgconf_paths = []
        for dep in self.dependencies.values():
            for subdir in ("lib", "share"):
                path = os.path.join(dep.package_folder, subdir, "pkgconfig")
                if os.path.isdir(path):
                    pkgconf_paths.append(path)

        pkgconf_path = ":".join(pkgconf_paths)
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        subprocess.run(
            f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder} -Denable-x11=false -Dxkb-config-root=/usr/share/X11/xkb -Dx-locale-root=/usr/share/X11/locale"',
            shell=True,
            check=True,
        )
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)


    def package_info(self):
        self.cpp_info.libs = ["xkbcommon", "xkbregistry"]
