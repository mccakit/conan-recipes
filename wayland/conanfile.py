from conan import ConanFile
import os
import subprocess
import shutil

class wayland(ConanFile):
    name = "wayland"
    version = "main"
    requires = ("libffi/[>3.5.2]", "libxml2/[>2.15]")

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
        pkgconf_path += ":" + os.path.join(str(utilities), "lib", "pkgconfig")
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        os.mkdir("scanner")
        subprocess.run(
            f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={os.path.abspath("scanner")} -Dlibraries=false -Dtests=false -Ddocumentation=false -Ddtd_validation=false"',
            shell=True,
            check=True,
        )
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)
        shutil.rmtree("builddir")

        paths = pkgconf_path.split(":")
        paths = paths[:-1]
        pkgconf_path = ":".join(paths)
        pkgconf_path += ":" + os.path.join(os.path.abspath("scanner"), "lib", "pkgconfig")
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        print(os.environ["PKG_CONFIG_LIBDIR"])
        subprocess.run(
            f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder}"',
            shell=True,
            check=True,
        )
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)


    def package_info(self):
        self.cpp_info.libs = ["wayland-client", "wayland-cursor", "wayland-egl", "wayland-server"]
