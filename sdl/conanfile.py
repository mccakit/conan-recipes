from conan import ConanFile
import os
import subprocess

class sdl(ConanFile):
    name = "sdl"
    version = "main"
    settings = "os", "arch", "compiler", "build_type"
    def requirements(self):
        if self.settings.os == "Linux":
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
        pkgconf_path = ":".join(
            [os.path.join(dep.package_folder, subdir)
             for dep in self.dependencies.values()
             for subdir in ["lib/pkgconfig", "lib/x86_64-linux-gnu/pkgconfig", "share/pkgconfig"]]
            + ["/usr/lib/x86_64-linux-gnu/pkgconfig", "/usr/share/pkgconfig"]
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DSDL_LIBICONV=OFF -DSDL_EXAMPLES=OFF -DSDL_LIBUDEV=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)
