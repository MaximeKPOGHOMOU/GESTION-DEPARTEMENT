[Setup]
AppName=Gestion Departement
AppVersion=1.0
DefaultDirName={pf}\Gestion Departement
DefaultGroupName=Nv(())
OutputDir=Output

[Files]
Source: "chemin_vers_votre_application\*"; DestDir: "{app}"

[Icons]
Name: "{group}\Nom de votre application"; Filename: "{app}\Nom_de_votre_application.exe"

[Files]
Source: "chemin_vers_votre_application\menuprincipal.py"; DestDir: "{app}"
Source: "chemin_vers_votre_application\etudiant.py"; DestDir: "{app}"
Source: "chemin_vers_votre_application\enseignant.py"; DestDir: "{app}"
