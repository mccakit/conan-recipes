from conan import ConanFile
import os
import subprocess
import shutil, glob


class uvw(ConanFile):
    name = "uvw"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    requires = (
        "libuv/v1.x",
    )
    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:skypjack/uvw.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        src_dir = os.path.join(self.source_folder, "uvw", "src", "uvw")
        dst_dir = os.path.join(self.package_folder, "include", "uvw")
        os.makedirs(dst_dir, exist_ok=True)
        for ext in ("*.hpp", "*.h", "*.ipp"):
            for f in glob.glob(os.path.join(src_dir, ext)):
                shutil.copy2(f, dst_dir)
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("uvw")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DUVW_USE_LIBCPP=OFF -DUVW_FETCH_LIBUV=OFF -DUVW_BUILD_TESTING=OFF -DUVW_BUILD_DOCS=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)
