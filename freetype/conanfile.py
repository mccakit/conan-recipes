from conan import ConanFile
from conan.tools.gnu import PkgConfigDeps
import os
import subprocess

class freetype(ConanFile):
    name = "freetype"
    requires = "libpng/[>1.7]"

    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:freetype/freetype.git -b {self.version}"', shell=True, check=True)

    def generate(self):
        deps = PkgConfigDeps(self)
        deps.generate()

    def build(self):
        meson_native = self.conf.get("user.mccakit:meson_native", None)
        meson_cross = self.conf.get("user.mccakit:meson_cross", None)
        os.chdir("freetype")

        os.environ["PKG_CONFIG_PATH"] = str(self.generators_folder)
        subprocess.run(f'bash -c "meson setup builddir --native-file={meson_native} --cross-file={meson_cross} --prefix={self.package_folder}"', shell=True, check=True)
        subprocess.run(f'bash -c "meson compile -C builddir"', shell=True, check=True)
        subprocess.run(f'bash -c "meson install -C builddir"', shell=True, check=True)

    def package_info(self):
        pass
