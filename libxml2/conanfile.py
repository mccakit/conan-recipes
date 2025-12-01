from conan import ConanFile
from conan.tools.gnu import PkgConfigDeps
import os
import subprocess

class libxml2_conan(ConanFile):
    name = "libxml2"
    requires = "icu/[>75]"

    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:GNOME/libxml2.git -b {self.version}"', shell=True, check=True)

    def generate(self):
        # Generate pkg-config files for ICU
        deps = PkgConfigDeps(self)
        deps.generate()

    def build(self):
        meson_native = self.conf.get("user.mccakit:meson_native", None)
        meson_cross = self.conf.get("user.mccakit:meson_cross", None)
        os.chdir("libxml2")

        # Set PKG_CONFIG_PATH so Meson can find ICU
        os.environ["PKG_CONFIG_PATH"] = str(self.generators_folder)
        subprocess.run(f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder} -Dicu=enabled"', shell=True, check=True)
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.set_property("pkg_config_name", "libxml-2.0")
        self.cpp_info.libs = ["xml2"]
        self.cpp_info.includedirs = ["include/libxml2"]
