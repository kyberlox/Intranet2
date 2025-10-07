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
iptables -A DOCKER-USER -p tcp --dport 22 -j ACCEPT
iptables -A DOCKER-USER -p tcp --dport 80 -j ACCEPT
iptables -A DOCKER-USER -p tcp --dport 443 -j ACCEPT

# Файл с IP-адресами администраторов
ADMIN_IPS_FILE="admin_ip.txt"

# Порта, которые нужно защитить (добавьте нужные вам порты)
PROTECTED_PORTS="5432 6379 8000 9200 9300 27017"

# Добавляем правила для каждого IP из файла
if [ -f "$ADMIN_IPS_FILE" ]; then
    while read ip; do
        # Пропускаем пустые строки и комментарии
        [[ -z "$ip" || "$ip" =~ ^# ]] && continue
        
        echo "Добавляем доступ для IP: $ip"
        for port in $PROTECTED_PORTS; do
            sudo iptables -I DOCKER-USER -p tcp --dport $port -s $ip -j ACCEPT
        done
    done < "$ADMIN_IPS_FILE"
else
    echo "Файл $ADMIN_IPS_FILE не найден!"
    exit 1
fi

# Блокируем доступ к защищаемым портам для всех остальных
for port in $PROTECTED_PORTS; do
    sudo iptables -A DOCKER-USER -p tcp --dport $port -j DROP
done

echo "Настройка завершена!"