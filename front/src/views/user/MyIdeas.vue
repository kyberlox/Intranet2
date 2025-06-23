<template>
    <div class="mt20">
        <h2 class="page__title">Есть идея! (Мои идеи)</h2>
        <div class="row mb-5">
            <div class="col">
                <RouterLink :to="{ name: 'newIdeaPage' }"
                            class="btn btn-primary"
                            data-toggle="tooltip"
                            data-placement="top"
                            title="Отправить новую идею!">Предложить идею</RouterLink>
            </div>
        </div>
        <div class="row mb-5">
            <div>
                <table class="table">
                    <tbody>
                        <tr>
                            <th>№</th>
                            <th>Дата</th>
                            <th>Название</th>
                            <th>Статус</th>
                        </tr>
                        <tr v-for="idea in ideas"
                            :key="idea.id">
                            <td>{{ idea.id }}</td>
                            <td>{{ idea.date }}</td>
                            <td>
                                <RouterLink :to="idea.href">Конкурс</RouterLink>
                            </td>
                            <td>{{ idea.status }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { ideas } from '@/assets/static/ideas';
export default defineComponent({
    name: 'MyIdeas',
    setup() {

        return {
            ideas
        };
    },
}); 
</script>