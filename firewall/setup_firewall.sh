#!/bin/bash

# Очистка старых правил в цепочке DOCKER-USER (осторожно!)
# Если вы не уверены, что цепочка DOCKER-USER пуста, то не очищайте ее, а вручную удалите только те правила, которые добавили вы.
# Вместо очистки мы можем пометить правила и удалить только их, но для простоты предположим, что мы хотим начать с чистого листа.

# ВНИМАНИЕ: Следующая команда удалит ВСЕ правила в цепочке DOCKER-USER.
# Если вы не хотите этого, закомментируйте эту строку.
iptables -F DOCKER-USER

# Разрешаем established и related соединения в начале цепочки.
iptables -I DOCKER-USER -m state --state ESTABLISHED,RELATED -j ACCEPT

# Разрешаем порты 80 и 443 для всех.
iptables -A DOCKER-USER -p tcp --dport 80 -j ACCEPT
iptables -A DOCKER-USER -p tcp --dport 443 -j ACCEPT

# Разрешаем все для IP-адресов из файла admin_ip.txt.
if [ -f admin_ip.txt ]; then
  while read ip; do
    # Пропускаем пустые строки и комментарии.
    [[ -z "$ip" || "$ip" =~ ^# ]] && continue
    iptables -A DOCKER-USER -s "$ip" -j ACCEPT
  done < admin_ip.txt
else
  echo "Файл admin_ip.txt не найден. Продолжаем без него." >&2
fi

# Блокируем весь остальной трафик в цепочке DOCKER-USER.
iptables -A DOCKER-USER -j DROP

echo "Правила настроены."