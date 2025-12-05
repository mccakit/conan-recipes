from conan import ConanFile
import os
import subprocess


class sdl_image(ConanFile):
    name = "sdl_image"
    version = "main"
    requires = (
        "sdl/[>=3.2.28]",
        "libpng/[>=1.7]",
        "libwebp/[>=1.6]",
        "libjpeg-turbo/[>=3.1.2]",
        "libiconv/[>1.18]",
        "zlib-ng/[>2.0.0]",
    )

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:libsdl-org/SDL_image.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("SDL_image")
        pkgconf_paths = []
        for dep in self.dependencies.values():
            for subdir in ("lib", "share"):
                path = os.path.join(dep.package_folder, subdir, "pkgconfig")
                if os.path.isdir(path):
                    pkgconf_paths.append(path)

        pkgconf_path = ":".join(pkgconf_paths)
        pkgconf_path = ":".join(["/usr/lib/x86_64-linux-gnu/pkgconfig"] + pkgconf_paths)
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        os.environ["LIBRARY_PATH"] = ":".join([
            os.path.join(self.dependencies['libiconv'].package_folder, 'lib')
        ])
        os.environ["CPATH"] = os.pathsep.join([
            os.path.join(self.dependencies['libiconv'].package_folder, 'include'),
        ])
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DSDLIMAGE_SAMPLES=OFF -DSDLIMAGE_AVIF=OFF -DSDLIMAGE_BMP=OFF -DSDLIMAGE_JPG_SHARED=OFF -DSDLIMAGE_PNG_SHARED=OFF -DSDLIMAGE_WEBP_SHARED=OFF -DSDLIMAGE_TIF=OFF -DSDLIMAGE_ZLIB_SHARED=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["SDL3_image"]
