{ pkgs, lib, ... }:

let
  libs = [
    pkgs.libGL
    pkgs.libGLU
    pkgs.libx11
    pkgs.libxext
    pkgs.libxcursor
    pkgs.libxi
    pkgs.libxfixes
    pkgs.libxrandr
    pkgs.libxrender
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.libdecor
    pkgs.dbus
    pkgs.alsa-lib
    pkgs.libpulseaudio
  ];
in
{
  packages = libs ++ [
    pkgs.uv
  ];

  env.PYOPENGL_PLATFORM = "glx";
  env.LD_LIBRARY_PATH = "${lib.makeLibraryPath libs}:/run/opengl-driver/lib";

  enterShell = ''
    export LD_LIBRARY_PATH="${lib.makeLibraryPath libs}:/run/opengl-driver/lib:$LD_LIBRARY_PATH"
  '';
}
