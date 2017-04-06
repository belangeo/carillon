import os, shutil

os.system('C:\Python27\Scripts\pyinstaller.exe --clean -F -w --icon=Resources\AppIcon.ico "Carillon.py"')

os.system("git checkout-index -a -f --prefix=Carillon_Win/")

os.system("copy dist\Carillon.exe Carillon_Win /Y")
os.remove("Carillon_Win/Carillon.py")

# Menage
shutil.rmtree("build")
shutil.rmtree("dist")
os.remove("Carillon.spec")