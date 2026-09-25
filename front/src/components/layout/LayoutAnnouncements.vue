<template>
    <section v-if="announcements.length" class="layout-announcements d-print-none" aria-label="Объявления">
        <article v-for="announcement in announcements" :key="announcement.id"
            class="layout-announcement"
            :class="announcement.type && `layout-announcement--${announcement.type}`">
            <h2 v-if="announcement.title" class="layout-announcement__title">{{ announcement.title }}</h2>
            <div class="layout-announcement__message-row">
                <svg v-if="announcement.type === 'warning'" class="layout-announcement__warning-icon"
                    viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" aria-hidden="true">
                    <path d="M12 3 2 21h20L12 3Z" />
                    <path d="M12 9v5" />
                    <path d="M12 18h.01" />
                </svg>
                <p class="layout-announcement__message">{{ announcement.message }}</p>
            </div>
        </article>
    </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';

export interface LayoutAnnouncement {
    id: string | number;
    title?: string;
    message: string;
    type?: 'info' | 'success' | 'warning' | 'error';
}

export default defineComponent({
    name: 'LayoutAnnouncements',
    props: {
        announcements: {
            type: Array as PropType<LayoutAnnouncement[]>,
            required: true,
        },
    },
});
</script>
