from conan import ConanFile
import os
import subprocess


class ICUConan(ConanFile):
    name = "icu"
    version = "main"
    requires = ()

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:unicode-org/icu.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
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

        os.chdir("icu/icu4c/source")
        os.mkdir("native")
        abs_native = os.path.abspath("native")
        os.chdir("native")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "source {autotools_native} && ../configure {static} && make -j{cpu_count}"',
            shell=True,
            check=True,
        )

        os.chdir("..")
        os.mkdir("cross")
        os.chdir("cross")
        subprocess.run(
            f'bash -c "source {autotools_cross} && ../configure --host={autotools_target} {type} --prefix={self.package_folder} --with-cross-build={abs_native} --disable-tools --disable-tests --disable-samples --disable-extras && make -j{cpu_count} && make install"',
            shell=True,
            check=True,
        )

    def package_info(self):
        self.cpp_info.libs = ["icuuc", "icudata", "icuio", "icui18n"]
