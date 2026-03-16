from conan import ConanFile
import os
import subprocess


class wayland_scanner(ConanFile):
    name = "wayland_scanner"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "libexpat/master",
    )

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
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_PATH"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "meson setup builddir --native-file={meson_native} --prefix={self.package_folder} -Dlibraries=false -Dscanner=true -Dtests=false -Ddocumentation=false -Ddocbook_validation=false -Ddtd_validation=false "',
            shell=True,
            check=True,
        )
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)
