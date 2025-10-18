# LAUNCHER CREATOR

A small tool to create and edit application launchers (.desktop files) for Linux.

Features
- Create, edit and validate .desktop launcher files.
- Set executable command, icon, categories, terminal usage and other standard keys.
- Provide a simple template for new launchers.
- Safe editing that preserves uncommon keys and comments.

Quick start
- Clone the repository and run the included launcher creator script or binary (see repository root for executable or scripts).
- Alternatively, edit .desktop files by using the provided template below and save as ~/.local/share/applications/<name>.desktop

.desktop template
[Desktop Entry]
Type=Application
Name=My Application
Comment=Short description of the application
Exec=/path/to/executable %U
Icon=/path/to/icon.png
Terminal=false
Categories=Utility;Application;
StartupNotify=true

Usage notes
- Place user-specific launchers in ~/.local/share/applications/ and system-wide launchers in /usr/share/applications/.
- Ensure the Exec path is executable and the Icon path is accessible by the desktop environment.
- Use %f, %F, %u, %U, %i, %c field codes in Exec as needed (see freedesktop.org desktop entry spec).

Installation
- If an install script is provided: run ./install.sh (may require sudo for system-wide install).
- Otherwise run the tool directly from the repository or copy the executable/script to a directory on your PATH.

Contributing
- Bug reports and pull requests are welcome. Follow repository coding style and include tests where appropriate.
- Provide clear commit messages and a short description in PRs.

License
- Include an open-source license file in the repository (MIT recommended if none exists).
- If a LICENSE file already exists, follow its terms.

References
- Desktop Entry Specification: https://specifications.freedesktop.org/desktop-entry-spec/latest/
- Application launcher locations: ~/.local/share/applications/ and /usr/share/applications/
- For more detailed behavior, check the repository files and docs included with this project.
