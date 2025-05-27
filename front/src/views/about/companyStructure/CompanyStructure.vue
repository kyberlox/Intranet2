<template>
    <div class="structure__wrapper mt20">
        <!-- Рекурсивный компонент для отображения иерархии -->
        <div v-if="hierarchyTree"
             class="hierarchy-container">
            <CompanyBlock :department="hierarchyTree"
                          :level="0" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import CompanyBlock from './CompanyBlock.vue';

export default defineComponent({
    components: {
        CompanyBlock
    },
    setup() {
        const structurePlug = [
            {
                "_index": "departs",
                "_id": "53",
                "_score": null,
                "_source": {
                    "join_field": {
                        "name": "department",
                        "parent": null
                    },
                    "name": "ЭМК",
                    "dep_id_for_sort": 53,
                    "user_head_id": 174,
                    "users": [
                        {
                            "user_id": 174,
                            "user_fio": "Кошкарев Виталий Алексеевич",
                            "user_position": "Руководитель ЭМК"
                        }
                    ]
                },
                "sort": [53]
            },
            {
                "_index": "departs",
                "_id": "54",
                "_score": null,
                "_source": {
                    "join_field": {
                        "name": "department",
                        "parent": 53
                    },
                    "name": "Дирекция по информационным технологиям ",
                    "dep_id_for_sort": 54,
                    "user_head_id": 124,
                    "users": [
                        {
                            "user_id": 124,
                            "user_fio": "Алешин Алексей Владимирович",
                            "user_position": "Директор"
                        },
                        {
                            "user_id": 4137,
                            "user_fio": "Кудрявцев Алексей Сергеевич",
                            "user_position": "Руководитель проектов ДИТ"
                        }
                    ]
                },
                "sort": [54]
            },
            {
                "_index": "departs",
                "_id": "55",
                "_score": null,
                "_source": {
                    "join_field": {
                        "name": "department",
                        "parent": 54
                    },
                    "name": "Отдел менеджмента ДИТ (ОМ)",
                    "dep_id_for_sort": 55,
                    "user_head_id": 2151,
                    "users": [
                        {
                            "user_id": 2151,
                            "user_fio": "Бурлов Олег Вячеславович",
                            "user_position": "Руководитель "
                        }
                    ]
                },
                "sort": [55]
            },
            {
                "_index": "departs",
                "_id": "56",
                "_score": null,
                "_source": {
                    "join_field": {
                        "name": "department",
                        "parent": 54
                    },
                    "name": "Отдел системного администрирования (ОСА)",
                    "dep_id_for_sort": 56,
                    "user_head_id": 60,
                    "users": [
                        {
                            "user_id": 60,
                            "user_fio": "Кудасова Ольга Александровна",
                            "user_position": "Руководитель"
                        },
                        {
                            "user_id": 3654,
                            "user_fio": "Митрофанов Александр Сергеевич",
                            "user_position": "Системный администратор сектора СКС"
                        },
                        {
                            "user_id": 101,
                            "user_fio": "Коротков Андрей Владимирович",
                            "user_position": "Архитектор СКС"
                        }
                    ]
                },
                "sort": [56]
            },
            {
                "_index": "departs",
                "_id": "59",
                "_score": null,
                "_source": {
                    "join_field": {
                        "name": "department",
                        "parent": 53
                    },
                    "name": "Дирекция по маркетингу",
                    "dep_id_for_sort": 59,
                    "user_head_id": 157,
                    "users": [
                        {
                            "user_id": 157,
                            "user_fio": "Друзина Ирина Алексеевна",
                            "user_position": "Директор по маркетингу"
                        },
                        {
                            "user_id": 1399,
                            "user_fio": "Горобец Анастасия Владиславовна",
                            "user_position": "Маркетолог"
                        },
                        {
                            "user_id": 3123,
                            "user_fio": "Брагин Иван Дмитриевич",
                            "user_position": "Стажер"
                        },
                        {
                            "user_id": 3542,
                            "user_fio": "Мирошникова Дарья Владимировна",
                            "user_position": "Руководитель медиа-проектов"
                        },
                        {
                            "user_id": 166,
                            "user_fio": "Ремизова Алла Львовна",
                            "user_position": "Координатор внешних образовательных программ"
                        },
                        {
                            "user_id": 1384,
                            "user_fio": "Пшеничных Мария Вячеславовна",
                            "user_position": "Ведущий маркетолог"
                        },
                        {
                            "user_id": 1748,
                            "user_fio": "Доценко Юлия Васильевна",
                            "user_position": "Маркетолог"
                        }
                    ]
                },
                "sort": [59]
            }
        ]

        const hierarchyTree = ref(null);

        onMounted(() => {
            makeHierarchy();
        })

        const makeHierarchy = () => {
            // Создаем индекс всех департаментов по ID
            const departmentMap = {};
            structurePlug.forEach((dept) => {
                departmentMap[dept._id] = {
                    id: dept._id,
                    name: dept._source.name,
                    users: dept._source.users,
                    parentId: dept._source.join_field.parent,
                    children: []
                };
            });

            // Находим корневой элемент и строим дерево
            let rootDepartment = null;

            Object.values(departmentMap).forEach((dept) => {
                if (dept.parentId === null) {
                    rootDepartment = dept;
                } else if (departmentMap[dept.parentId]) {
                    departmentMap[dept.parentId].children.push(dept);
                }
            });

            hierarchyTree.value = rootDepartment;
            console.log(hierarchyTree.value);
        }

        return {
            hierarchyTree
        }
    }
})
</script>