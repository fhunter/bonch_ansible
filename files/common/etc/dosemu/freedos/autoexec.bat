@echo off
rem autoexec.bat for DOSEMU + FreeDOS
path z:\bin;z:\gnu;z:\dosemu;f:\borlandc\bin;f:\prolog;f:\vc
set HELPPATH=z:\help
set TEMP=c:\tmp
blaster
prompt $P$G
unix -s DOSDRIVE_D
if "%DOSDRIVE_D%" == "" goto nodrived
lredir del d: > nul
lredir d: linux\fs%DOSDRIVE_D%
:nodrived
lredir del t: > nul
lredir t: linux\fs/tmp
lredir del f: > nul
lredir f: linux\fs/afs/dcti.sut.ru/soft/dosroot/
set TEMP=t:\
rem uncomment to load another bitmap font
rem loadhi display con=(vga,866,2)
rem mode con codepage prepare=((866) z:\cpi\ega.cpx)
rem mode con codepage select 866
rem chcp 866
lredir e: linux\fs/media/cdrom c
unix -s DOSEMU_VERSION
echo "Welcome to dosemu %DOSEMU_VERSION%!"
unix -e
d:
f:\keyrus
vc
