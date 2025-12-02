from conan import ConanFile
import os
import subprocess

class wayland_protocols(ConanFile):
    name = "wayland-protocols"
    version = "main"
    requires = ("wayland/[>=1.24]")

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 https://gitlab.freedesktop.org/wayland/wayland-protocols.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        meson_native = self.conf.get("user.mccakit:meson_native", None)
        meson_cross = self.conf.get("user.mccakit:meson_cross", None)

        os.chdir("wayland-protocols")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder}"',
            shell=True,
            check=True,
        )
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)


    def package_info(self):
        self.cpp_info.libs = ["wayland"]
