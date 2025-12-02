from conan import ConanFile
import os
import subprocess

class zstd_conan(ConanFile):
    name = "zstd"
    version = "dev"
    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:facebook/zstd.git -b {self.version}"', shell=True, check=True)

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        build = self.conf.get("user.mccakit:build", None)
        if build == "static":
            btype_opt = "-DZSTD_BUILD_SHARED=OFF -DZSTD_BUILD_STATIC=ON"
        elif build == "shared":
            btype_opt = "-DZSTD_BUILD_SHARED=ON -DZSTD_BUILD_STATIC=OFF"
        else:
            raise ValueError("Invalid build type")
        os.chdir("zstd")
        subprocess.run(f'bash -c "cmake -B build -G Ninja -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DZSTD_BUILD_PROGRAMS=OFF -DZSTD_BUILD_DEPRECATED=OFF -DZSTD_LEGACY_SUPPORT=OFF {btype_opt}"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --build build --parallel"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)
    def package_info(self):
        self.cpp_info.libs = ["zstd"]
