import PhoneIcon from "@/assets/icons/layout/sidebar/socLinks/PhoneIcon.svg";
import VkIcon from "@/assets/icons/layout/sidebar/socLinks/VkIcon.svg";
import TelegramIcon from "@/assets/icons/layout/sidebar/socLinks/TelegramIcon.svg";
import EmkLogo from "@/assets/icons/layout/sidebar/socLinks/EmkLogo.svg";
import DocsIcon from "@/assets/icons/layout/sidebar/socLinks/DocsIcon.svg";
import MotiwIcon from "@/assets/icons/layout/sidebar/workLinks/MotiwIcon.svg";
import BitrixIcon from "@/assets/icons/layout/sidebar/workLinks/BitrixIcon.svg";

import type { WorkLink, SupportLink } from "@/interfaces/ILayoutSideBar";

export const workLinks: WorkLink[] = [
    {
        title: "Мотив",
        href: "http://motiw.imp.int/user/",
        description: "Задачи",
        linkTitle: "К задачам",
        icon: MotiwIcon,
    },
    {
        title: "Битрикс24",
        href: "https://portal.emk.ru/",
        description: "Задачи",
        linkTitle: "К задачам",
        icon: BitrixIcon,
    },
];

export const supportLinks: SupportLink[] = [
    {
        title: "1277",
        href: "tel:#1277",
        description: "Тех. поддержка сайта",
        icon: PhoneIcon,
    },
    {
        title: "Мы в VK",
        href: "https://vk.com/npo_emk",
        description: "https://vk.com/npo_emk",
        icon: VkIcon,
    },
    {
        title: "Мы в Telegram",
        href: "https://t.me/emk_emk",
        description: "@emk_emk",
        icon: TelegramIcon,
    },
    {
        title: "Наш сайт",
        href: "http://www.emk.ru/",
        description: "http://www.emk.ru",
        icon: EmkLogo,
    },
    {
        title: "Редактор Интранет",
        href: "",
        description: "Перейти",
        icon: DocsIcon,
    },
];