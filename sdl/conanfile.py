from conan import ConanFile
import os
import subprocess

class sdl(ConanFile):
    name = "sdl"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("libiconv/[>=1.16]")
            self.requires("alsa-lib/[>=1.0]")
            self.requires("wayland/[>=1.24]")
            self.requires("wayland-protocols/[>=1.46]")
            self.requires("vulkan-headers/[>=1.4.3]")
            self.requires("libxkbcommon/[>=1.13]")
        elif self.settings.os == "Android":
            self.requires("vulkan-headers/[>=1.4.3]")

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:libsdl-org/SDL.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("SDL")
        pkgconf_paths = []
        for dep in self.dependencies.values():
            for subdir in ("lib", "share"):
                path = os.path.join(dep.package_folder, subdir, "pkgconfig")
                if os.path.isdir(path):
                    pkgconf_paths.append(path)

        pkgconf_path = ":".join(pkgconf_paths)
        if self.settings.os == "Linux":
            pkgconf_path = ":".join(["/usr/lib/x86_64-linux-gnu/pkgconfig"] + pkgconf_paths)
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        if self.settings.os == "Linux":
            os.environ["LIBRARY_PATH"] = ":".join([
                os.path.join(self.dependencies['libiconv'].package_folder, 'lib')
            ])
            os.environ["CPATH"] = os.pathsep.join([
                os.path.join(self.dependencies['libiconv'].package_folder, 'include'),
            ])
            os.environ["PATH"] = (
                os.path.join(self.dependencies["wayland"].package_folder, "bin")
                + os.pathsep +
                os.environ["PATH"]
            )
        os.environ["CPATH"] = os.pathsep.join([
            os.path.join(self.dependencies['vulkan-headers'].package_folder, 'include')
        ])
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DSDL_LIBICONV=ON -DSDL_EXAMPLES=OFF -DSDL_LIBUDEV=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["SDL3"]
