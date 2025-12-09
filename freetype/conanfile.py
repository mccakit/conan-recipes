from conan import ConanFile
import os
import subprocess

class freetype(ConanFile):
    name = "freetype"
    version = "master"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "brotli/[>1.2.0]",
        "libpng/[>1.7]",
        "zlib-ng/[>2.0.0]",
    )

    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:freetype/freetype.git -b {self.version}"', shell=True, check=True)

    def build(self):
        meson_native = self.conf.get("user.mccakit:meson_native", None)
        meson_cross = self.conf.get("user.mccakit:meson_cross", None)
        os.chdir("freetype")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder} -Dharfbuzz=disabled -Dbzip2=disabled -Dzlib=system"', shell=True, check=True)
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["freetype"]
