<template>
  <div class="mt-20">
    <button @click="handleTypeClick('news')"> К новостям </button>
    <button @click="handleTypeClick('blogs')"> К блогам </button>
    <button @click="handleTypeClick('interview')"> К интервью </button>
    <button @click="handleTypeClick('noPreview')"> Без превью </button>
  </div>
  <Transition :name="previewFullWidth ? 'layout-change' : 'layout-change-toLeft'"
              mode="out-in">
    <div class="admin-panel__editor__element-inner__wrapper mt20"
         :class="{ 'admin-panel__editor__element-inner__wrapper--previewFullWidth': previewFullWidth }"
         :key="previewFullWidth ? 'fullwidth' : 'normal'">
      <div class="admin-panel__editor__element-inner"
           :class="[{ 'admin-panel__editor__element-inner--previewFullWidth': previewFullWidth }, { 'admin-panel__editor__element-inner--noPreview': activeType == 'noPreview' }]">
        <div v-for="(item, index) in sampleEvent"
             class="admin-panel__editor__element-inner__field"
             :class="{ 'admin-panel__editor__element-inner__field--previewFullWidth': previewFullWidth }"
             :key="index">
          <div v-if="item.type == 'date' && item.name"
               class="no-transition">
            <p>{{ item.title }}</p>
            <DatePicker class="noTransition"
                        v-model="currentItem[item.name]" />
          </div>
          <div v-else-if="item.type == 'select' && item.name">
            <p>{{ item.title }}</p>
            <select v-model="currentItem[item.name]">
              <option v-for="(option, index) in item.options"
                      :key=index>
                {{ option }}
              </option>
            </select>
          </div>
          <div v-else-if="item.type == 'textWithRedact' && item.name">
            <p>{{ item.title }}</p>
            <TextEditor v-model="currentItem[item.name]" />
          </div>
          <div v-else-if="item.type == 'auto'">
            <p>{{ item.title }}</p>
            <p>{{ item.value }}</p>
          </div>
          <div v-else-if="item.type == 'text' && item.name">
            <p>{{ item.title }}</p>
            <input v-model="currentItem[item.name]"
                   :disabled="Boolean(item.disabled)" />
          </div>
          <div v-else-if="item.type == 'img'">
            <p>{{ item.title }}</p>
            <div class="attached__gallery">
              <div v-for="(itemInner, index) in item.value"
                   :key="index"
                   class="attached__gallery__card">
                <img v-if="typeof itemInner == 'string'"
                     :src="itemInner"
                     class="attached__gallery__card-img"
                     alt="Изображение элемента" />
                <div v-if="typeof itemInner == 'string'"
                     class="attached__gallery__card-icons">
                  <button class="icon-button view-button"
                          @click.prevent="goToImage(itemInner)">
                    <ZoomIcon />
                  </button>
                  <button class="icon-button delete-button"
                          @click.prevent="removeItem(itemInner)">
                    <CloseIcon />
                  </button>
                </div>
              </div>
            </div>
            <ImgUploader />
          </div>
          <div v-else-if="item.type == 'doc'">
            <p>{{ item.title }}</p>
            <div class="attached__gallery--doc">
              <a v-for="(item, index) in currentItem.documents"
                 class="attached__gallery--doc__item"
                 :key="index"
                 :href="item"
                 target='_blank'>
                {{ item }}
              </a>
            </div>
            <FileUploader />
          </div>
        </div>
      </div>
      <div class="admin-panel__editor__element-inner__preview"
           :class="{ 'admin-panel__editor__element-inner__preview--previewFullWidth': previewFullWidth }">
        <Transition name="layout-change"
                    mode="out-in">
          <LayoutTop v-if="previewFullWidth"
                     class="zoom--preview"
                     @click="previewFullWidth = !previewFullWidth" />
          <LayoutLeft v-else
                      class="zoom--preview"
                      @click="previewFullWidth = !previewFullWidth" />
        </Transition>
        <PostInner v-if="currentItem.id && activeType == 'news'"
                   :previewElement="currentItem"
                   :type="'adminPreview'" />
        <Interview v-if="activeType == 'interview'"
                   :interviewInner="currentItem" />
        <CertainBlog v-if="activeType == 'blogs'"
                     :interviewInner="currentItem"
                     :id="String(15238)"
                     :authorId="String(157)" />
      </div>
    </div>
  </Transition>

  <div class="save-button__wrapper">
    <button class="save-button">
      <span class="save-button__text">Сохранить</span>
    </button>
    <button class="save-button">
      <span class="save-button__text">Отменить</span>
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import TextEditor from '@/components/admin/TextEditor.vue';
import ImgUploader from '@/components/admin/ImgUploader.vue';
import FileUploader from '@/components/admin/FileUploader.vue';
import CloseIcon from "@/assets/icons/admin/CloseIcon.svg?component";
import LayoutLeft from "@/assets/icons/admin/LayoutLeft.svg?component";
import LayoutTop from "@/assets/icons/admin/LayoutTop.svg?component";
import { sampleEvent } from '@/assets/staticJsons/adminPagePlugs';
import DatePicker from '@/components/DatePicker.vue';
import PostInner from '@/components/PostInner.vue';
import Interview from '@/components/about/ourPeople/Interview.vue';
import CertainBlog from '../about/blogs/CertainBlog.vue';
import ZoomIcon from '@/assets/icons/admin/ZoomIcon.svg?component'

type AdminElementValue = string | number | string[] | boolean | undefined | Array<{ link: string; name: string }>;
interface IAdminElement extends Record<string, AdminElementValue> {
  id: number;
}

export default defineComponent({
  components: {
    TextEditor,
    FileUploader,
    ImgUploader,
    CloseIcon,
    LayoutLeft,
    LayoutTop,
    DatePicker,
    PostInner,
    Interview,
    CertainBlog,
    ZoomIcon
  },
  props: {
    id: {
      type: String
    },
    elementId: {
      type: String
    }
  },
  setup(props) {
    const events = ref<Event[]>([]);
    const router = useRouter();
    const currentItem: Ref<IAdminElement> = ref({ id: 0 });
    const previewItem = ref();
    const previewFullWidth = ref(false);

    onMounted(() => {
      sampleEvent.map((e) => {
        if (!e.name) return;
        currentItem.value[e.name] = e.value;
      })

      previewItem.value = {
        indirect_data: currentItem.value
      }
    })

    const removeItem = (e: string) => {
      alert('udalit ' + e);
    }

    const activeType = ref('news');

    const handleTypeClick = (type: string) => {
      activeType.value = type;
    }

    return {
      events,
      sampleEvent,
      router,
      goToImage: (e: string) => window.open(e, '_blank'),
      removeItem,
      currentItem,
      previewFullWidth,
      handleTypeClick,
      activeType
    };
  }
});
</script>

<style lang="scss" scoped>
.admin-panel__editor__element-inner {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 33%;

  &__preview {
    max-width: 100%;
    overflow-wrap: break-word;
    user-select: none;
  }

  &--previewFullWidth {
    align-items: center;
  }
}

.admin-panel__editor__element-inner__wrapper {
  display: flex;
  flex-direction: row;
  gap: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;


  &--previewFullWidth {
    flex-direction: column-reverse;
  }
}

.admin-panel__editor__element-inner__field {
  min-width: 250px;
  max-width: 500px;
  width: 100%;
}

p {
  margin: 0;
  padding: 0;
  font-weight: 500;
  margin-bottom: 8px;
}

/* Standard input styling */
input[type="text"],
input[type="file"],
select,
input:not([type]) {
  width: 100%;
  height: 40px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

input[type="file"] {
  padding: 6px;
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23131313%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 10px;
  padding-right: 30px;
}

:deep(.p-editor-container) {
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 100%;
}

:deep(.p-editor-toolbar) {
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
  padding: 8px;
}

:deep(.ql-formats button) {
  margin-right: 5px;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.admin-panel__editor__element-inner__field div[v-else-if="item.type == 'auto'"] p:last-child {
  padding: 8px 12px;
  background-color: #f9f9f9;
  border: 1px solid #eee;
  border-radius: 4px;
  min-height: 40px;
  display: flex;
  align-items: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* Action buttons */
.action-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary {
  background-color: #4a6cf7;
  color: white;
  border: none;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.attached__gallery {
  display: grid;
  gap: 5px;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
}

.attached__gallery__card {
  width: 100%;
  object-fit: contain;
  aspect-ratio: 16 / 9;
  position: relative;
}

.attached__gallery__card-img {
  width: 100%;
  height: 100%;
  position: absolute;
}

.attached__gallery--doc {
  display: flex;
  flex-direction: column;

  &__item {
    color: blue;
    transition: 0.1s;

    &:hover {
      color: orange
    }
  }
}

// иконки
.attached__gallery__card-icons {
  position: absolute;
  top: 5px;
  right: 5px;
  display: flex;
  gap: 5px;
}

.icon-button {
  color: white;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-button {
  background-color: #ff4d4f;
  color: white;
}

.view-button {
  background-color: #1890ff;
  color: white;
}

.icon-button:hover {
  transform: scale(1.1);
}

.admin-panel__editor__element-inner__preview {
  overflow: hidden;
  flex-grow: 1;
  height: fit-content;
  position: sticky;
  top: 100px;

  &--previewFullWidth {
    position: relative;
    top: auto;
  }
}

.zoom--preview {
  position: absolute;
  width: 25px;
  right: 0;
  transition: 0.2s;

  &:hover {
    color: var(--emk-brand-color);
    cursor: pointer;
  }
}

.admin-panel__editor__element-inner__field--previewFullWidth {
  max-width: 50%;
}

.admin-panel__editor__element-inner--previewFullWidth {
  align-content: center;
  align-items: center;
  border-top: 1px solid gainsboro;
  padding-top: 40px;
}

.layout-change-enter-active,
.layout-change-leave-active,
.layout-change-toLeft-enter-active,
.layout-change-toLeft-leave-active {
  transition: all 0.2s ease;
}

.layout-change-enter-from,
.layout-change-leave-to {
  opacity: 0.7;
  transform: translateX(-30px);
}

.layout-change-toLeft-enter-from,
.layout-change-toLeft-leave-to {
  opacity: 0.7;
  transform: translateX(30px);
}

// save-btn
.save-button__wrapper {
  margin: auto;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.save-button {
  background-color: var(--emk-brand-color);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 20px;
  min-width: 120px;

  &:hover {
    transform: translateY(-1px);
    background: #6ed110;
  }

  &:active {
    transform: translateY(0);
  }

  &:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.3);
  }
}

.noTransition {
  transition: none !important;
}

.admin-panel__editor__element-inner--noPreview {
  width: 100%;
  align-items: center;
}
</style>
