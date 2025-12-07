from conan import ConanFile
import os
import subprocess


class lua(ConanFile):
    name = "lua"
    version = "5.5.0-rc2"
    extract = "lua-5.5.0"
    requires = ()
    def source(self):
        archive = f"lua-{self.version}.tar.gz"
        url = f"https://www.lua.org/work/{archive}"
        subprocess.run(
            f'bash -c "curl -L -R -O {url} && tar -xzf {archive}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        autotools_native = self.conf.get("user.mccakit:autotools_native", None)
        autotools_cross = self.conf.get("user.mccakit:autotools_cross", None)
        autotools_target = self.conf.get("user.mccakit:autotools_target", None)
        build = self.conf.get("user.mccakit:build", None)
        os.chdir(f"lua-{self.version.split('-')[0]}")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            [
                "bash",
                "-c",
                f'source {autotools_cross} && make linux CC="$CC" AR="$AR rcs" RANLIB="$RANLIB" MYCFLAGS="$CFLAGS" MYLDFLAGS="$LDFLAGS" && make install INSTALL_TOP={self.package_folder}'
            ],
            check=True,
        )

    def package_info(self):
        self.cpp_info.libs = ["lua"]
