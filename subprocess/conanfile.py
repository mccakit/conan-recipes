from conan import ConanFile
import os
import subprocess as sp
import shutil, glob

class subprocess(ConanFile):
    name = "subprocess"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
        pass

    def source(self):
        sp.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:mccakit/subprocess.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("subprocess")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        sp.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DBUILD_TESTING=OFF"',
            shell=True,
            check=True,
        )
        sp.run(f'bash -c "cmake --build build --parallel"', shell=True, check=True)
        sp.run(f'bash -c "cmake --install build"', shell=True, check=True)
