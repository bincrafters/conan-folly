#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration
import os


class FollyConan(ConanFile):
    name = "folly"
    version = "2018.10.15.00"
    description = "An open-source C++ library developed and used at Facebook"
    url = "https://github.com/bincrafters/conan-folly"
    homepage = "https://github.com/facebook/folly"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "Apache-2.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "folly.patch"]
    generators = "cmake"
    requires = (
        "boost/1.68.0@conan/stable",
        "double-conversion/3.1.1@bincrafters/stable",
        "gflags/2.2.1@bincrafters/stable",
        "glog/0.3.5@bincrafters/stable",
        "libevent/2.1.8@bincrafters/stable",
        "lz4/1.8.3@bincrafters/stable",
        "OpenSSL/1.0.2o@conan/stable",
        "zlib/1.2.11@conan/stable",
        "zstd/1.3.5@bincrafters/stable",
    )
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           Version(self.settings.compiler.version.value) < "14":
            raise ConanInvalidConfiguration("Folly could not be built by Visual Studio < 14")
    
    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + '-' + self.version
        os.rename(extracted_dir, self._source_subfolder)
        
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake
        
    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file='folly.patch')
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "dl"])
        elif not self.options.shared and self.settings.compiler == "Visual Studio":
            self.cpp_info.libs.extend(["ws2_32", "Iphlpapi", "Crypt32"])