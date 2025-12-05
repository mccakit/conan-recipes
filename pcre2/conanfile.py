from conan import ConanFile
import os
import subprocess
from packaging.version import Version, InvalidVersion

class pcre2(ConanFile):
    name = "pcre2"
    version = "main"
    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:PCRE2Project/pcre2.git -b {self.version}"', shell=True, check=True)
    def build(self):
        autotools_native = self.conf.get("user.mccakit:autotools_native", None)
        autotools_cross = self.conf.get("user.mccakit:autotools_cross", None)
        autotools_target = self.conf.get("user.mccakit:autotools_target", None)
        cpu_count = os.cpu_count() or 0
        cpu_count -= 1
        build = self.conf.get("user.mccakit:build", None)
        static = "--enable-static --disable-shared"
        shared = "--enable-shared --disable-static"
        if build == "static":
            type = static
        elif build == "shared":
            type = shared
        else:
            raise ValueError("Invalid build type")
        os.chdir("pcre2")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(f'bash -c "autoreconf -i"', shell=True, check=True)
        subprocess.run(f'bash -c "source {autotools_native} && ./configure --prefix {self.package_folder} --host={autotools_target} {type} && make -j{cpu_count} && make install"', shell=True, check=True)
