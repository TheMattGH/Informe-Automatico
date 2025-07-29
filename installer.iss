[Setup]
AppName=Generador de Informes Automático
AppVersion=1.0
DefaultDirName={pf}\Generador De Informes
DefaultGroupName=Generador de Informes Automático
OutputDir=dist
DisableDirPage=no
OutputBaseFilename=Instalador Generador De Informes
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\Generador de Informes.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Generador de Informes Automático"; Filename: "{app}\Generador de Informes.exe"
Name: "{userdesktop}\Generador de Informes Automático"; Filename: "{app}\Generador de Informes.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Opciones adicionales:"