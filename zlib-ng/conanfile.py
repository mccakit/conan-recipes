from conan import ConanFile
import os
import subprocess

class zlib_ng(ConanFile):
    name = "zlib-ng"
    version= "develop"
    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:zlib-ng/zlib-ng.git -b {self.version}"', shell=True, check=True)

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        build = self.conf.get("user.mccakit:build", None)
        os.chdir("zlib-ng")
        subprocess.run(f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH={self.generators_folder} -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DBUILD_TESTING=OFF -DZLIB_COMPAT=ON"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --build build --parallel"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)
    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["z"]
