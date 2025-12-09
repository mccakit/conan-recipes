from conan import ConanFile
import os
import subprocess


class opusfile(ConanFile):
    name = "opusfile"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("opus/[>=1.5.2]")
        elif self.settings.os == "Android":
            self.requires("opus/[>=1.5.2]")
            self.requires("ogg/[>=1.3.6]")
            self.requires("boringssl/[>0.20]")

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:mccakit/opusfile.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("opusfile")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder}"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["opusfile", "opusurl"]
