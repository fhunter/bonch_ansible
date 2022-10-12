#!/bin/bash

# Смена владельца на root:documents
chown root:documents -R /home/homes/documents/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-rwx -R /home/homes/documents/
# Разрешение на чтение группе documents_ro
setfacl -m g:documents_ro:rX -R -P /home/homes/documents/

#find /home/homes/documents/ -type f -print0|xargs -0 chmod ug+rw

# Смена владельца на root:termpapers_rw
chown root:termpapers_rw -R /home/homes/term_projects/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-rwx -R /home/homes/term_projects/
# Разрешение на чтение группе documents_ro
setfacl -m g:termpapers_ro:rX -R -P /home/homes/term_projects/

# Смена владельца на root:materials
chown root:materials -R /home/homes/materials/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-w,o+rX -R /home/homes/materials/

# Смена владельца на root:books
chown root:materials -R /home/homes/books/
# Запрет записи всем кроме владельца и группы
chmod ug+rwX,o-w,o+rX -R /home/homes/books/
