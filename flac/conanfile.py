from conan import ConanFile
import os
import subprocess


class flac(ConanFile):
    name = "flac"
    version = "master"
    settings = "os", "arch", "compiler", "build_type"
    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("ogg/[>=1.3.6]")
            self.requires("libiconv/[>1.18]")
        elif self.settings.os == "Android":
            pass

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:xiph/flac.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("flac")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        os.environ["LIBRARY_PATH"] = ":".join(
            [os.path.join(self.dependencies["libiconv"].package_folder, "lib")]
        )
        os.environ["CPATH"] = os.pathsep.join(
            [os.path.join(self.dependencies["libiconv"].package_folder, "include")]
        )
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DINSTALL_MANPAGES=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["FLAC", "FLAC++"]
