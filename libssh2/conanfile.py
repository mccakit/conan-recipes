from conan import ConanFile
import os
import subprocess

class libssh2(ConanFile):
    name = "libssh2"
    version = "master"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "boringssl/[>0.20]",
        "zlib/[>1.3.1]",
    )

    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:libssh2/libssh2.git -b {self.version}"', shell=True, check=True)

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("libssh2")
        pkgconf_path = ":".join(os.path.join(dep.package_folder, "lib", "pkgconfig") for dep in self.dependencies.values())
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(dep.package_folder for dep in self.dependencies.values())
        subprocess.run(f'bash -c "cmake -B builddir -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DLIBSSH2_BUILD_DOCS=OFF"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --build builddir --parallel"', shell=True, check=True)
        subprocess.run(f'bash -c "cmake --install builddir"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["ssh2"]
