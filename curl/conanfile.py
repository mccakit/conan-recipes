from conan import ConanFile
import os
import subprocess


class curl(ConanFile):
    name = "curl"
    version = "master"
    settings = "os", "arch", "compiler", "build_type"
    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("boringssl/[>0.20]")
            self.requires("libidn2/[>2.8.3]")
            self.requires("zstd/[>1.5.7]")
            self.requires("zlib-ng/[>2.0.0]")
            self.requires("brotli/[>1.2.0]")
            self.requires("libpsl/[>0.21.5]")
            self.requires("libssh2/[>1.11.1]")
        elif self.settings.os == "Android":
            self.requires("boringssl/[>0.20]")
            self.requires("zstd/[>1.5.7]")
            self.requires("zlib-ng/[>2.0.0]")
            self.requires("brotli/[>1.2.0]")
            self.requires("libssh2/[>1.11.1]")


    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:curl/curl.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("curl")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        if self.settings.os == "Linux":
            subprocess.run(
                f'bash -c "cmake -B builddir -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DBUILD_CURL_EXE=OFF -DUSE_LIBIDN2=OFF"',
                shell=True,
                check=True,
            )
        elif self.settings.os == "Android":
            subprocess.run(
                f'bash -c "cmake -B builddir -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DBUILD_CURL_EXE=OFF -DCURL_USE_LIBPSL=OFF"',
                shell=True,
                check=True,
            )
        subprocess.run(
            f'bash -c "cmake --build builddir --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install builddir"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["curl"]
