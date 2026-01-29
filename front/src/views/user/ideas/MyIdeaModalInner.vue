<template>
<div class="modal__text">
    <div v-if="currentUser"
         class="modal__text__content">
        <div class="row mb-3">
            <div class="col">
                <img :src="currentUser.photo_file_url"
                     class="img-fluid img-thumbnail modal__text__content__user-photo rounded-circle mx-auto d-block">
                <div class="text-center mt20">
                    <strong>{{ currentUser.last_name + " " + currentUser.name + " " +
                        currentUser.second_name }}</strong><br>
                    <span class="fw-light">{{ currentUser.indirect_data?.work_position }}</span><br>
                    <span v-for="(item, index) in currentUser.indirect_data?.uf_usr_1696592324977"
                          :key="'depart' + index">
                        {{ item }}
                    </span>
                </div>
            </div>
        </div>
        <div class="row mb-3 justify-content-center">
            <div class="col-sm-10 col-print-12">
                <h2 class="page__title text-center">#{{ textContent?.number }} {{ textContent?.name }}
                </h2>
                <div v-if="textContent?.content"
                     class="mb-3 modal__text__content__detail">
                    <span>
                        {{ textContent.content }}
                    </span>
                </div>
                <div class="mb-3 modal__text__content__detail modal__text__content__detail--link">
                    <a v-if="textContent?.files"
                       :href="textContent.files.file_url">
                        <span>
                            {{ textContent.files.original_name }}
                        </span>
                    </a>
                </div>
                <div>
                    <div :href="`https://portal.emk.ru/intranet/editor/feedback/pdfgen.php?ELEMENT_ID=${textContent?.id}`"
                         target="_blank"
                         @click="savePdf"
                         class="primary-button">Сохранить PDF</div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>


<script lang="ts">
import type { IBXFileType } from '@/interfaces/IEntities';
import type { IPostIdeaPdf } from '@/interfaces/IPostFetch';
import Api from '@/utils/Api';
import download from 'downloadjs';
import { defineComponent, type PropType } from 'vue';

interface IUserForModal {
    photo_file_url: string
    last_name: string
    name: string
    second_name: string
    indirect_data?: {
        work_position?: string
        uf_usr_1696592324977?: string[]
    }
}

interface IModalTextContent {
    id: string
    number: string
    name: string
    content: string
    files: IBXFileType
    user_id: string
}

export default defineComponent({
    props: {
        currentUser: {
            type: Object as PropType<IUserForModal>,
        },
        textContent: {
            type: Object as PropType<IModalTextContent>,
        }
    },
    setup(props) {
        console.log(props);

        const savePdf = () => {
            const ideaTitle = `#${props.textContent?.number} ${props.textContent?.name}`;
            const ideaContent = props.textContent?.content ?? '';

            const body: IPostIdeaPdf = {
                user_id: props.textContent?.user_id,
                name: ideaTitle,
                description: ideaContent
            }

            Api.post('idea_pdf/generate_pdf', body, { responseType: 'blob' })
                .then((data) => {
                    download(new Blob([data.data]), ideaTitle + '.pdf', 'application/pdf')
                })

            // Api.get('/idea_pdf/generate_pdf/2')
        }
        return {
            savePdf
        }
    }
})
</script>