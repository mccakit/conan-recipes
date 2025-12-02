from conan import ConanFile
import os
import subprocess


class brotli(ConanFile):
    name = "brotli"
    version = "master"
    requires = ()

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:google/brotli.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("brotli")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder}"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = [
            "brotlicommon",
            "brotlienc",
            "brotlidec",
        ]
