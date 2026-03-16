from conan import ConanFile
import os
import subprocess
import shutil

class wayland(ConanFile):
    name = "wayland"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    requires = ("libexpat/master", "wayland_scanner/main", "libffi/master")

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 https://gitlab.freedesktop.org/wayland/wayland.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        meson_native = self.conf.get("user.mccakit:meson_native", None)
        meson_cross = self.conf.get("user.mccakit:meson_cross", None)
        utilities = self.conf.get("user.mccakit:utilities", None)

        os.chdir("wayland")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, subdir)
            for dep in self.dependencies.values()
            for subdir in ["lib/pkgconfig", "lib/x86_64-linux-gnu/pkgconfig"]
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder} -Dscanner=false -Dtests=false -Dtests=false -Ddocumentation=false"',
            shell=True,
            check=True,
        )
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)
