export DMG_DIR="Carillon 0.1"
export DMG_NAME="Carillon_0.1.dmg"


python setup.py py2app

rm -rf build
mv dist Carillon_OSX

if cd Carillon_OSX;
then
    find . -name .git -depth -exec rm -rf {} \
    find . -name *.pyc -depth -exec rm -f {} \
    find . -name .* -depth -exec rm -f {} \;
else
    echo "Something wrong. Carillon_OSX not created"
    exit;
fi

rm Carillon.app/Contents/Resources/AppIcon.ico

# keep only 64-bit arch
ditto --rsrc --arch x86_64 Carillon.app Carillon-x86_64.app
rm -rf Carillon.app
mv Carillon-x86_64.app Carillon.app

# Fixed wrong path in Info.plist
cd Carillon.app/Contents
awk '{gsub("Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python", "@executable_path/../Frameworks/Python.framework/Versions/2.7/Python")}1' Info.plist > Info.plist_tmp && mv Info.plist_tmp Info.plist

cd ../../..
cp -R Carillon_OSX/Carillon.app .

echo "assembling DMG..."
mkdir "$DMG_DIR"
cd "$DMG_DIR"
cp -R ../Carillon.app .
ln -s /Applications .

cd ..

hdiutil create "$DMG_NAME" -srcfolder "$DMG_DIR"

rm -rf "$DMG_DIR"
rm -rf Carillon_OSX
rm -rf Carillon.app