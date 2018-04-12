Date: 2017-10-17 11:43
Category: Personal
Title: Не надо бояться отдыхать
Tags: productivity, experience, work, discipline

Чем старше становлюсь, тем яснее понимаю, что не надо бояться отдыхать. Не надо пытаться сделать всё и сразу. Не надо бояться декомпозиции, итеративного подхода.

Вот яркий пример разницы в коде, который пишется вечером:

```
l = float(len(i))

hlmin = int(math.floor(l/2))  # Get indexes of pre/post-middle digits
hlmax = int(math.ceil(l/2))

a = i[:hlmin]                 # Get first/last half of number
b = i[hlmax:][::-1]

if a == b:                    # Is palyndrome
    return True
```

... и утром:

```
if i == i[::-1]:             # Is palyndrome
    return True
```

Вот этот [коммит](https://github.com/agrrh/lychrel/commit/ff4d9ed6d85da6e78f0a007cf87da96f203bf4bd?diff=split). Код ищет числа-палиндромы.

Из той же копилки откровенно идиотских решений (а я тогда работал в действительно крупной и известной компании):

```
if os.path.isfile(copy_path):
    pass
else:
    pass
```

До сих пор не могу пояснить, что хотел здесь сделать, но точно помню, что засиживался допоздна.

Вывод простой: спокойно обдумывать шаги и только после этого решительно их предпринимать, не наоборот. :)
