Title: Не надо бояться отдыхать
Date: 2017-10-17 11:43
Tags: productivity, experience, work, discipline

Чем старше становлюсь, тем яснее понимаю, что не надо бояться отдыхать. Не надо пытаться сделать всё и сразу. Не надо бояться декомпозиции, итеративного подхода.

Вот яркий пример разницы в коде, который пишется вечером и утром:

![preview]({filename}/media/idiotic-comparsion.png)

Вот этот [https://github.com/agrrh/lychrel/commit/ff4d9ed6d85da6e78f0a007cf87da96f203bf4bd?diff=split](коммит).

```
# before
l = float(len(i))
hlmin = int(math.floor(l/2))  # Get indexes of pre/post-middle digits
hlmax = int(math.ceil(l/2))
a = i[:hlmin]  # Get first/last half of number
b = i[hlmax:][::-1]
if a == b:
    return True

# after
if i == i[::-1]:
    return True
```

Из той же копилки откровенно идиотских решений (а я тогда работал в действительно крупной и известной компании):

```
if os.path.isfile(copy_path):
    pass
else:
    pass
```

До сих пор не могу пояснить, что хотел здесь сделать, но точно помню, что засиживался допоздна.
