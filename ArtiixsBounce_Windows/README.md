# Artiixs Bounce — Windows build files

This package contains the Windows-specific source and a build script. It does **not** include a prebuilt `.exe`, because a real Windows executable should be built on Windows (or a Windows CI runner), not claimed as built from this Linux environment.

## Build on Windows 10

1. Install Python 3.12 from https://www.python.org/downloads/windows/
2. During setup, enable **Add python.exe to PATH**.
3. Extract this folder.
4. Double-click `build_windows.bat`.
5. The executable will be at `dist\ArtiixsBounce.exe`.

## Behavior and caveats

- Global key presses create animated characters near the mouse pointer.
- Active characters follow the current mouse pointer during their animation.
- Escape exits.
- The overlay attempts to be transparent and click-through on Windows.
- This is an early prototype. Global keyboard hooks may be restricted by security software, and Windows display/scaling setups can affect overlay positioning.
- Only use it on a computer where you have permission to run global keyboard hooks.

## Cloud build option

The `.github/workflows/build.yml` workflow can build the executable on a Windows GitHub Actions runner. Put these files in a GitHub repository, then use **Actions → Build Windows EXE → Run workflow**. Download the `ArtiixsBounce-Windows` artifact from that workflow run.
