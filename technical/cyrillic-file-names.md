Title: Broken cyrillic names under Linux
Date: 2015-08-28 18:18
Tags: mount, convmv, encodings

Кажется, что-то из этого я применял в бытность работы саппортом в хвостинге.

Если имя файла выглядит, как последовательность знаков вопроса - может помочь утилита `convmv`:

```bash
convmv -f cp1251 -t koi8 -r ./
convmv -f cp1251 -t koi8 -r ./ --notest
```

Первый прогон тестовый, покажет, что будет изменено, далее применяем правки с флагом `--notest`.

А так можно поправить имена файлов из zip-архива, созданного под Windows:

```bash
convmv -f cp1252 -t cp850 ./ --notest
convmv -f cp866 -t utf-8 ./ --notest
```

Есть похожая проблема с монтированием FAT32-разделов, решением будет указать кодовую страницу и принудительно выставить кодирование в UTF-8:

```bash
mount /dev/sdx1 /mnt/test -t vfat -o iocharset=cp1251,codepage=866,utf8=true
```

Ссылки, где черпал инфу:

- [http://najomi.org/_nix/convmv](http://najomi.org/_nix/convmv)
- [http://www.gamedev.ru/flame/forum/?id=13379](http://www.gamedev.ru/flame/forum/?id=13379)
