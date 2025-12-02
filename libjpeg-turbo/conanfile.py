from conan import ConanFile
import os
import subprocess

class libjpeg_turbo(ConanFile):
    name = "libjpeg-turbo"
    version = "main"
    requires = ()
    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:libjpeg-turbo/libjpeg-turbo.git -b {self.version}"', shell=True, check=True)

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        build = self.conf.get("user.mccakit:build", None)
        os.chdir("libjpeg-turbo")
        if(build == "static"):
            btypeopt = "-DENABLE_SHARED=OFF -DENABLE_STATIC=ON"
        elif(build == "shared"):
            btypeopt = "-DENABLE_SHARED=ON -DENABLE_STATIC=OFF"
        else:
            raise ValueError("Invalid build type")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} {btypeopt} -DWITH_TOOLS=OFF"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --build build --parallel"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["jpeg", "turbojpeg"]
