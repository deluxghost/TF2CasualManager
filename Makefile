.PHONY: all zip soft_clean clean

all: dist\tf2cm.exe
	mkdir dist\tf2cm
	mkdir dist\tf2cm\data
	mkdir dist\tf2cm\data\images
	copy /y dist\tf2cm.exe dist\tf2cm
	del /f /q dist\tf2cm.exe
	copy /y data\README.txt dist\tf2cm
	copy /y data\tf2cm_default.json dist\tf2cm\data
	copy /y data\casual.min.json dist\tf2cm\data
	copy /y data\images\*.* dist\tf2cm\data\images

zip: all
	cd dist && zip -r tf2cm.zip tf2cm
	rd /s /q dist\tf2cm

dist\tf2cm.exe: soft_clean project\icon\icon.ico tf2cm.py
	pyinstaller -F -w --icon="project\icon\icon.ico" tf2cm.py

soft_clean:
	if exist dist (rd /s /q dist)

clean: soft_clean
	if exist build (rd /s /q build)
	del /f /q tf2cm.spec >nul 2>&1
