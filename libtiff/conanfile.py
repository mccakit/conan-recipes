from conan import ConanFile
import os
import subprocess


class libtiff(ConanFile):
    name = "libtiff"
    version = "master"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "zstd/[>1.5.7]",
        "zlib-ng/[>2.0.0]",
        "libjpeg_turbo/[>3.1.2]",
        "xz/[>5.8]",
        "lerc/[>=4.0.0]",
        "libwebp/[>1.6]",
        "jbigkit/[>=2.1]",
    )

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:libsdl-org/libtiff.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        build = self.conf.get("user.mccakit:build", None)
        os.chdir("libtiff")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        os.environ["LDFLAGS"] = "-lsharpyuv"
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_INSTALL_PREFIX={self.package_folder} -Dtiff-tools=OFF -Dtiff-tests=OFF -Dtiff-docs=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["tiff"]
