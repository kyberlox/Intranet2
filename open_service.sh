#!/bin/bash

# Скрипт для ограничения доступа к портам Docker только для конкретного IP
# Использование: sudo bash open_service.sh -p PORT -i IP

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Переменные
PORT=""
IP=""
SERVICE_NAME=""

# Функции для вывода
log() { echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"; }
error() { echo -e "${RED}[ОШИБКА] $1${NC}"; exit 1; }
warning() { echo -e "${YELLOW}[ПРЕДУПРЕЖДЕНИЕ] $1${NC}"; }
info() { echo -e "${BLUE}[INFO] $1${NC}"; }

# Показать справку
show_help() {
    cat << EOF
Использование: $0 -p PORT -i IP

ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ:
    -p PORT    Номер порта для настройки (например: 5432, 6379, 27017)
    -i IP      IP-адрес, который нужно разрешить (например: 178.178.208.163)

ПРИМЕРЫ:
    sudo $0 -p 5432 -i 178.178.208.163
    sudo $0 -p 6379 -i 192.168.1.100
    sudo $0 -p 27017 -i 10.0.0.50

ОПИСАНИЕ:
    Этот скрипт настраивает брандмауэр для ограничения доступа к указанному порту
    только для одного конкретного IP-адреса. Работает с Docker портами.
    Все остальные подключения блокируются.
EOF
}

# Парсинг аргументов
parse_arguments() {
    while getopts "p:i:h" opt; do
        case $opt in
            p)
                PORT="$OPTARG"
                ;;
            i)
                IP="$OPTARG"
                ;;
            h)
                show_help
                exit 0
                ;;
            \?)
                error "Неверный аргумент. Используйте -h для справки."
                ;;
            :)
                error "Аргумент -$OPTARG требует значение."
                ;;
        esac
    done
    
    if [[ -z "$PORT" || -z "$IP" ]]; then
        error "Не указаны обязательные параметры. Используйте -h для справки."
    fi
}

# Проверка прав root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Этот скрипт должен быть запущен с правами root: sudo bash $0"
    fi
}

# Валидация порта
validate_port() {
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
        error "Некорректный номер порта: $PORT. Должен быть от 1 до 65535."
    fi
}

# Валидация IP-адреса
validate_ip() {
    if ! [[ "$IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        error "Некорректный формат IP-адреса: $IP"
    fi
}

# Определение имени сервиса
get_service_name() {
    case $PORT in
        22) SERVICE_NAME="SSH" ;;
        80) SERVICE_NAME="HTTP" ;;
        443) SERVICE_NAME="HTTPS" ;;
        5432) SERVICE_NAME="PostgreSQL" ;;
        6379) SERVICE_NAME="Redis" ;;
        27017) SERVICE_NAME="MongoDB" ;;
        3306) SERVICE_NAME="MySQL" ;;
        1433) SERVICE_NAME="MSSQL" ;;
        *) SERVICE_NAME="порт $PORT" ;;
    esac
}

# Проверка Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker не установлен"
    fi
}

# Полная очистка старых правил для Docker портов
cleanup_old_docker_rules() {
    log "Очистка старых правил для порта $PORT в цепочке DOCKER-USER..."
    
    # Удаляем все правила для порта в цепочке DOCKER-USER
    iptables -L DOCKER-USER --line-numbers -n 2>/dev/null | grep "dpt:$PORT" | awk '{print $1}' | tac | while read -r num; do
        if [[ -n "$num" ]]; then
            iptables -D DOCKER-USER "$num" 2>/dev/null || true
        fi
    done
    
    # Удаляем UFW правила если есть
    ufw status numbered | grep " $PORT/" | awk -F"[][]" '{print $2}' | tac | while read -r num; do
        if [[ -n "$num" ]]; then
            echo "y" | ufw delete "$num" 2>/dev/null || true
        fi
    done
    
    log "Старые правила очищены"
}

# Проверка существования цепочки DOCKER-USER
ensure_docker_user_chain() {
    if ! iptables -L DOCKER-USER > /dev/null 2>&1; then
        log "Цепочка DOCKER-USER не найдена, создаем..."
        iptables -N DOCKER-USER
        iptables -I FORWARD -j DOCKER-USER
    fi
}

# Настройка правил iptables для Docker портов
setup_docker_iptables() {
    log "Настройка правил iptables в цепочке DOCKER-USER для порта $PORT..."
    
    ensure_docker_user_chain
    
    # Удаляем стандартное правило RETURN если оно мешает (временно)
    iptables -D DOCKER-USER -j RETURN 2>/dev/null || true
    
    # Сначала разрешаем для конкретного IP
    iptables -I DOCKER-USER -p tcp -s "$IP" --dport "$PORT" -j ACCEPT
    
    # Затем запрещаем для всех остальных
    iptables -I DOCKER-USER -p tcp --dport "$PORT" -j DROP
    
    # Возвращаем правило RETURN в конец
    iptables -A DOCKER-USER -j RETURN
    
    log "Правила iptables для Docker применены: порт $PORT открыт только для $IP"
}

# Дополнительная настройка UFW для не-Docker сервисов
setup_ufw_fallback() {
    if command -v ufw &> /dev/null; then
        log "Дополнительная настройка UFW..."
        
        if ! ufw status | grep -q "Status: active"; then
            ufw --force enable
        fi
        
        ufw allow from "$IP" to any port "$PORT"
        log "Дополнительные правила UFW применены"
    fi
}

# Проверка Docker контейнеров использующих порт
check_docker_containers() {
    log "Поиск Docker контейнеров использующих порт $PORT..."
    
    local containers=$(docker ps --format "table {{.Names}}\t{{.Ports}}" | grep ":$PORT" || true)
    
    if [[ -n "$containers" ]]; then
        info "Найдены контейнеры использующие порт $PORT:"
        echo "$containers"
    else
        warning "Не найдено Docker контейнеров использующих порт $PORT"
    fi
}

# Сохранение правил iptables
save_iptables_rules() {
    log "Сохранение правил iptables..."
    
    if command -v iptables-save &> /dev/null; then
        mkdir -p /etc/iptables
        iptables-save > /etc/iptables/rules.v4
        
        # Создаем службу для восстановления правил при загрузке
        create_iptables_service
        
        log "Правила сохранены в /etc/iptables/rules.v4"
    else
        warning "iptables-save не найден, правила не сохранены"
    fi
}

# Создание службы для восстановления правил
create_iptables_service() {
    local service_file="/etc/systemd/system/iptables-docker-rules.service"
    
    cat > "$service_file" << EOF
[Unit]
Description=Restore iptables rules for Docker ports
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'sleep 10 && iptables-restore /etc/iptables/rules.v4'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl enable iptables-docker-rules.service 2>/dev/null && \
    log "Служба восстановления правил создана" || \
    warning "Не удалось создать службу восстановления правил"
}

# Проверка примененных правил
verify_rules() {
    log "Проверка примененных правил..."
    
    echo -e "\n${BLUE}=== Правила в цепочке DOCKER-USER для порта $PORT ===${NC}"
    if iptables -L DOCKER-USER -n 2>/dev/null | grep -E "($PORT|$IP)" | grep -v "chain"; then
        iptables -L DOCKER-USER -n --line-numbers | grep -E "($PORT|$IP)" | grep -v "chain"
    else
        warning "Правила в DOCKER-USER не найдены"
    fi
    
    echo -e "\n${BLUE}=== Статус порта $PORT ===${NC}"
    if command -v ss &> /dev/null; then
        ss -tlnp | grep ":$PORT " && log "Порт $PORT слушает подключения" || warning "Порт $PORT не слушает"
    elif command -v netstat &> /dev/null; then
        netstat -tlnp | grep ":$PORT " && log "Порт $PORT слушает подключения" || warning "Порт $PORT не слушает"
    else
        warning "Не найдены утилиты для проверки портов"
    fi
    
    echo -e "\n${BLUE}=== Docker контейнеры на порту $PORT ===${NC}"
    docker ps --format "table {{.Names}}\t{{.Ports}}" | grep ":$PORT" || warning "Контейнеры не найдены"
}

# Тестирование доступности
test_access() {
    log "Информация для тестирования..."
    
    local server_ip=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')
    
    echo -e "\n${YELLOW}Для тестирования выполните:${NC}"
    echo "С разрешенного IP ($IP):"
    echo "  nmap -p $PORT $server_ip"
    echo "  telnet $server_ip $PORT"
    
    echo -e "\nС другого IP (должен быть закрыт):"
    echo "  nmap -p $PORT $server_ip"
}

# Основная функция
main() {
    log "Начало настройки ограничения доступа к Docker порту $PORT для IP $IP"
    
    parse_arguments "$@"
    check_root
    validate_port
    validate_ip
    get_service_name
    check_docker
    
    info "Настройка $SERVICE_NAME (порт $PORT) для доступа только с IP: $IP"
    
    # Основные шаги
    cleanup_old_docker_rules
    setup_docker_iptables
    setup_ufw_fallback
    check_docker_containers
    save_iptables_rules
    verify_rules
    test_access
    
    log "Настройка завершена успешно!"
    log "Docker порт $PORT ($SERVICE_NAME) теперь доступен только с IP: $IP"
    
    echo -e "\n${GREEN}✓ Готово! Docker порт заблокирован для внешнего доступа.${NC}"
}

# Обработка сигналов
trap 'error "Прервано пользователем"; exit 1' INT TERM

# Запуск скрипта
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi