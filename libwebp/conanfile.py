from conan import ConanFile
import os
import subprocess


class libwebp(ConanFile):
    name = "libwebp"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "zlib-ng/[>2.0.0]",
        "libjpeg_turbo/[>3.1.2]",
        "libpng/[>1.7.0]",
    )

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:webmproject/libwebp.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("libwebp")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_INSTALL_PREFIX={self.package_folder}"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["webp", "sharpyuv", "webpdecoder", "webpmux", "webpdemux"]
