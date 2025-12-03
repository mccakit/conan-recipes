from conan import ConanFile
import os
import subprocess


class sdl_mixer(ConanFile):
    name = "sdl-mixer"
    version = "main"
    requires = (
        "sdl/[>=3.2.28]",
        "opus/[>=1.5.2]",
        "flac/[>=1.5]",
        "mpg123/[>=1.3]",
    )

    def source(self):
        subprocess.run(
            f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:libsdl-org/SDL_mixer.git -b {self.version}"',
            shell=True,
            check=True,
        )

    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        os.chdir("SDL_mixer")
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
        subprocess.run(
            f'bash -c "cmake -B build -G Ninja -DCMAKE_PREFIX_PATH=\\"{cmake_prefix_path}\\" -DCMAKE_TOOLCHAIN_FILE={cmake_toolchain} -DCMAKE_INSTALL_PREFIX={self.package_folder} -DSDLMIXER_GME=OFF -DSDLMIXER_MOD_XMP=OFF -DSDLMIXER_FLAC_LIBFLAC_SHARED=OFF -DSDLMIXER_MP3_MPG123_SHARED=OFF -DSDLMIXER_OPUS_SHARED=OFF"',
            shell=True,
            check=True,
        )
        subprocess.run(
            f'bash -c "cmake --build build --parallel"', shell=True, check=True
        )
        subprocess.run(f'bash -c "cmake --install build"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["SDL3_mixer"]
