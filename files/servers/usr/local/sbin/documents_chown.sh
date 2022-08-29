#!/bin/bash

# Смена владельца на root:documents
chown root:documents -R /afs/dcti.sut.ru/documents/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-rwx -R /afs/dcti.sut.ru/documents/
# Разрешение на чтение группе documents_ro
setfacl -m g:documents_ro:rX -R -P /afs/dcti.sut.ru/documents/

#find /afs/dcti.sut.ru/documents/ -type f -print0|xargs -0 chmod ug+rw

# Смена владельца на root:termpapers_rw
chown root:termpapers_rw -R /afs/dcti.sut.ru/term_projects/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-rwx -R /afs/dcti.sut.ru/term_projects/
# Разрешение на чтение группе documents_ro
setfacl -m g:termpapers_ro:rX -R -P /afs/dcti.sut.ru/term_projects/

# Смена владельца на root:materials
chown root:materials -R /afs/dcti.sut.ru/materials/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-w,o+rX -R /afs/dcti.sut.ru/materials/

# Смена владельца на root:books
chown root:materials -R /afs/dcti.sut.ru/books/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-w,o+rX -R /afs/dcti.sut.ru/books/
