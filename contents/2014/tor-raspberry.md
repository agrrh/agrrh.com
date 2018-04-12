Date: 2014-10-22 17:48
Modified: 2015-07-28 17:42
Category: Technical
Title: Делаем на основе Raspberry Pi и TOR анонимную точку доступа
Tags: raspberry pi, tor, anonymous

Данная статья была впервые опубликована на [Хабре](http://habrahabr.ru/post/241257/).

Привет, хабр!

От использования сети TOR меня удерживала необходимость каждый раз иметь дело с программными настройками, хотелось какого-то более общего решения, вынесенного за пределы используемого ПК. На днях я наткнулся на [этот проект](https://www.kickstarter.com/projects/augustgermar/anonabox-a-tor-hardware-router) и понял, что он решил бы все мои затруднения. Но так как проект был [заморожен](http://www.tomshardware.com/news/anonabox-tor-kickstarter-suspended-router,27919.html), в целях эксперимента в голову пришла идея создать такую точку доступа самому.

Теперь вот этот Raspberry Pi (ну, красненький!) раздает анонимный интернет в рамках моей квартиры:

![preview]({filename}/media/tor_raspberry.jpg)

В этой статье я расскажу, как научил свою «малину» выполнять функции точки доступа с направлением всего TCP-трафика через сеть TOR. Прошу под кат.

### Подготовка

Итак, что же нам потребуется:

- 1 x Raspberry Pi
- 1 x USB WiFi-адаптер

Свои Raspberry Pi я покупал [здесь](http://thepihut.com/collections/raspberry-pi), однако в доставке в Российскую Федерацию было отказано с отсылкой на «too unpredictable post service», так что для многих удобней будет воспользоваться следующим магазином или найти что-то третье.

WiFi-адаптер был выбран вот такой — [Nano WiFi Dongle](https://www.modmypi.com/raspberry-pi-accessories/networking/wireless-usb-1n-nano-adaptor-802.11N-wifi-dongle).

Начнем настройку, исходя из того, что на «малину» уже установлена ОС Raspbian. Предустановленный актуальный образ всегда можно получить на [официальном сайте устройства](http://www.raspberrypi.org/downloads/) или же пройти весь процесс с нуля, скачав [установщик](http://www.raspbian.org/RaspbianInstaller).

Первым делом подключаем устройство к проводной сети и ставим необходимое ПО, прочие пакеты либо уже установлены в системе, либо будут установлены по зависимостям:

    apt-get update
    # При желании - актуализируем ОС
    #apt-get upgrade -y
    apt-get install -y tor isc-dhcp-server hostapd iptables-persistent

На этом подготовительная часть завершена.

### Настройка точки доступа

Физически подключаем WiFi-адаптер и добавляем в файл ``/etc/network/interfaces` строки:

    auto wlan0
    iface wlan0 inet static
      address 192.168.55.1
      netmask 255.255.255.0

Настраиваем hostapd — демон, превращающий наше устройство в точку доступа. Для начала указываем путь к конфигурационному файлу в `/etc/default/hostapd`:

    DAEMON_CONF="/etc/hostapd/hostapd.conf"

Далее заполняем уже сам файл настроек, `/etc/hostapd/hostapd.conf`:

    interface=wlan0
    # имя нашей беспроводной сети
    ssid=anonymous_ap
    hw_mode=g
    # Предварительно рекомендуется выявить минимально загруженный канал
    channel=11
    # Фильтрация по MAC-адресам в данном примере отключена
    macaddr_acl=0
    # Для организации закрытой сети следует выставить эту опцию в значение 1 и раскомментировать нижеследующие строки
    wpa=0
    #wpa_key_mgmt=WPA-PSK
    #wpa_pairwise=TKIP CCMP
    #wpa_ptk_rekey=600
    # Собственно, задаем пароль
    #wpa_passphrase=hidemyass

Немного нетривиально производится активация стандарта 802.11n, которую данный адаптер поддерживает:

    # iwgetid --protocol wlan0
    wlan0     Protocol Name:"IEEE 802.11bgn"

Простое изменение параметра `hw_mode` в значение «n» привело к отрицательному результату, беспроводное соединение не поднялось после перезапуска:

    # /etc/init.d/hostapd restart
    [ ok ] Stopping advanced IEEE 802.11 management: hostapd.
    [FAIL] Starting advanced IEEE 802.11 management: hostapd failed!
    # tail /var/log/syslog | grep 'anonymous-ap'
    Oct 21 09:31:37 anonymous-ap ifplugd(mon.wlan0)[7490]: Link beat lost.
    Oct 21 09:31:38 anonymous-ap ifplugd(mon.wlan0)[7490]: Exiting.
    Oct 21 09:31:38 anonymous-ap ifplugd(wlan0)[1684]: Link beat lost.
    Oct 21 09:31:48 anonymous-ap ifplugd(wlan0)[1684]: Executing '/etc/ifplugd/ifplugd.action wlan0 down'.
    Oct 21 09:31:49 anonymous-ap ifplugd(wlan0)[1684]: Program executed successfully.

[Оказывается](http://wireless.kernel.org/en/users/Documentation/hostapd), `hw_mode` следует оставить в значении «g», но добавить строку `ieee80211n=1`, что и делаем, попутно перезапуская демон:

    \echo -e "\nieee80211n=1" >> /etc/hostapd/hostapd.conf

    service hostapd restart

Далее производим настройку DHCP, редактируя файл `/etc/dhcp/dhcpd.conf`:

    # Домен нашей сети
    option domain-name "anonymous-ap.local";

    # Параметры подсети
    subnet 192.168.55.0 netmask 255.255.255.0 {
      range 192.168.55.10 192.168.55.100;
      option domain-name-servers 8.8.4.4, 8.8.4.4;
      option routers 192.168.55.1;
      interface wlan0;
    }

Не забываем перезапустить сервис:

    /etc/init.d/isc-dhcp-server restart

### Настройка TOR

Весьма проста, т.к. мы не используем устройство в качестве точки выхода или relay-сервера, только осуществляем вход в сеть TOR. Для этого приведем файл `/etc/tor/torrc` к такому виду:

    VirtualAddrNetwork 172.16.0.0/12
    AutomapHostsSuffixes .onion,.exit
    AutomapHostsOnResolve 1
    TransPort 9040
    TransListenAddress 192.168.55.1
    DNSPort 53
    DNSListenAddress 192.168.55.1

### Настройка форвардинга пакетов

Быстро активируем форвардинг на уровне ядра:

    echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf
    sysctl -p

Настраиваем iptables для направления всего клиентского tcp-трафика в сеть TOR, оставляя доступ по SSH и DNS-запросы:

    iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 22 -j REDIRECT --to-ports 22
    iptables -t nat -A PREROUTING -i wlan0 -p udp --dport 53 -j REDIRECT --to-ports 53
    iptables -t nat -A PREROUTING -i wlan0 -p tcp --syn -j REDIRECT --to-ports 9040
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

    # Сохраняем правила в ранее установленный iptables-persistent, который сохранит их после перезагрузки
    iptables-save > /etc/iptables/rules.v4

Строго говоря, есть и иные варианты конфигурирования. Так, можно настроить точку доступа на простой форвардинг пакетов в «обычную» сеть при сохранении доступа к псевдо-доменам в зоне ".onion". [Подробнее здесь](https://trac.torproject.org/projects/tor/wiki/doc/TransparentProxy).

### Завершение и проверка

После чисто формальной перезагрузки наше устройство будет готово раздавать анонимный интернет:

    shutdown -r now

Теперь попробуем подключиться с ноутбука, телефона или планшета, а визит на [эту страницу](https://check.torproject.org/) позволит определить, все ли настроено корректно, вот пример сообщения об успехе:

![preview]({filename}/media/tor_success.png)

Надо заметить, что в реальности сервис проверки TOR, скорее всего, дополнительно предложит Вам установить [Tor Browser Bundle](https://www.torproject.org/projects/torbrowser.html.en) и это не случайно. Важно понимать, что само по себе использование сети TOR не даст полной гарантии анонимности и такие браузеры, как IE, Chrome и Safari вполне могут продолжать отправлять какие-либо сведения о пользователе.

Кроме того, подобный метод ни в коем случае не гарантирует полной защиты, для более надежной анонимизации следует изучить [вот эту](https://trac.torproject.org/projects/tor/wiki) подборку статей.

Надеюсь, рецепт будет полезен, буду рад дополнениям!
