from conan import ConanFile
import os
import subprocess

class ffmpeg(ConanFile):
    name = "ffmpeg"
    version = "master"
    def source(self):
        subprocess.run(f'bash -c "git clone --recurse-submodules --shallow-submodules --depth 1 git@github.com:FFmpeg/FFmpeg.git -b {self.version}"', shell=True, check=True)
    def build(self):
        cmake_toolchain = self.conf.get("user.mccakit:cmake", None)
        autotools_native = self.conf.get("user.mccakit:autotools_native", None)
        autotools_cross = self.conf.get("user.mccakit:autotools_cross", None)
        autotools_target = self.conf.get("user.mccakit:autotools_target", None)
        ffmpeg_target = self.conf.get("user.mccakit:ffmpeg_target", None)
        ffmpeg_arch = self.conf.get("user.mccakit:ffmpeg_arch", None)

        cpu_count = os.cpu_count() or 0
        cpu_count -= 1
        build = self.conf.get("user.mccakit:build", None)
        static = "--enable-static --disable-shared"
        shared = "--enable-shared --disable-static"
        if build == "static":
            type = static
        elif build == "shared":
            type = shared
        else:
            raise ValueError("Invalid build type")
        os.chdir("FFmpeg")
        pkgconf_path = ":".join(
            os.path.join(dep.package_folder, "lib", "pkgconfig")
            for dep in self.dependencies.values()
        )
        os.environ["PKG_CONFIG_LIBDIR"] = pkgconf_path
        cmake_prefix_path = ";".join(
            dep.package_folder for dep in self.dependencies.values()
        )
        subprocess.run(f'bash -c "source {autotools_cross} && ./configure --enable-cross-compile --arch={ffmpeg_arch} --target-os={ffmpeg_target} --cc=clang --as=clang --nm=llvm-nm --ar=llvm-ar --prefix={self.package_folder} {type} --disable-programs --disable-decoder=mlp --disable-encoder=mlp --disable-parser=mlp --disable-demuxer=mlp && make -j{cpu_count} && make install"', shell=True, check=True)

    def package_info(self):
        self.cpp_info.libs = ["avcodec", "avdevice", "avfilter", "avformat", "avutil", "swscale", "swresample"]
