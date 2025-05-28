import ECourses from "@/assets/icons/trainingCenter/ECourses.svg?component";
import Events from "@/assets/icons/trainingCenter/Events.svg?component";
import Announces from "@/assets/icons/trainingCenter/Announces.svg?component";
import Excursions from "@/assets/icons/trainingCenter/Excursions.svg?component";
import Literature from "@/assets/icons/trainingCenter/Literature.svg?component";
import Memo1C from "@/assets/icons/trainingCenter/Memo1C.svg?component";

import type { ITrainingSections } from "@/interfaces/ITrainingSections";

export const sectionsJson: ITrainingSections[] = [
    {
        name: "Электронные курсы",
        link: "Ecources",
        component: ECourses,
    },
    {
        name: "Проведенные тренинги",
        link: "conductedTrainings",
        component: Events,
    },
    {
        name: "Анонс учебных программ",
        link: "trainingAnnounces",
        component: Announces,
    },
    {
        name: "Экскурсии",
        link: "excursions",
        component: Excursions,
    },
    {
        name: "Учебные пособия и литература ЭМК",
        link: "literature",
        component: Literature,
    },
    {
        name: "Инструкция по работе 1С",
        link: "memo1c",
        component: Memo1C,
    },
];
