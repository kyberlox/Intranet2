<template>
  <div class="admin-panel__editor__element-inner__wrapper mt20"
       :class="{ 'admin-panel__editor__element-inner__wrapper--previewFullWidth': previewFullWidth }">
    <div class="admin-panel__editor__element-inner">
      <div v-for="(item, index) in sampleEvent"
           class="admin-panel__editor__element-inner__field"
           :key="index">
        <div v-if="item.type == 'date'">
          <p>{{ item.title }}</p>
          <DatePicker v-model="currentItem[item.name]" />
        </div>
        <div v-if="item.type == 'select'">
          <p>{{ item.title }}</p>
          <select v-model="currentItem[item.name]">
            <option v-for="(option, index) in item.options"
                    :key=index>
              {{ option }}
            </option>
          </select>
        </div>
        <div v-else-if="item.type == 'textWithRedact'">
          <p>{{ item.title }}</p>
          <TextEditor v-model="currentItem[item.name]" />
        </div>
        <div v-else-if="item.type == 'auto'">
          <p>{{ item.title }}</p>
          <p>{{ item.value }}</p>
        </div>
        <div v-else-if="item.type == 'text'">
          <p>{{ item.title }}</p>
          <input v-model="currentItem[item.name]"
                 :disabled="item.disabled" />
        </div>
        <div v-else-if="item.type == 'img'">
          <p>{{ item.title }}</p>
          <div class="attached__gallery">
            <div v-for="(item, index) in item.value"
                 :key="index"
                 class="attached__gallery__card">
              <img :src="item"
                   class="attached__gallery__card-img" />
              <!-- иконки -->
              <div class="attached__gallery__card-icons">
                <button class="icon-button view-button"
                        @click.prevent="goToImage(item)">
                  <ZoomIcon />
                </button>
                <button class="icon-button delete-button"
                        @click.prevent="removeItem(index)">
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
            <a v-for="(item, index) in item.attached"
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
    <div class="admin-panel__editor__element-inner__preview">
      <ZoomIcon class="zoom--preview"
                @click="previewFullWidth = !previewFullWidth" />
      <PostInner v-if="currentItem.id"
                 :previewElement="currentItem"
                 :type="'adminPreview'" />
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import TextEditor from '@/components/admin/TextEditor.vue';
import ImgUploader from '@/components/admin/ImgUploader.vue';
import FileUploader from '@/components/admin/FileUploader.vue';
import CloseIcon from "@/assets/icons/admin/CloseIcon.svg?component";
import ZoomIcon from "@/assets/icons/admin/ZoomIcon.svg?component";
import { sampleEvent } from '@/assets/staticJsons/adminPagePlugs';
import DatePicker from '@/components/DatePicker.vue';
import PostInner from '@/components/PostInner.vue';

export default defineComponent({
  components: {
    TextEditor,
    FileUploader,
    ImgUploader,
    CloseIcon,
    ZoomIcon,
    DatePicker,
    PostInner
  },
  setup() {
    const events = ref<Event[]>([]);
    const router = useRouter();
    const currentItem = ref({});
    const previewFullWidth = ref(false);

    onMounted(() => {
      sampleEvent.map((e) => {
        currentItem.value[e.name] = e.value;
      })
      console.log(currentItem.value);

    })


    const removeItem = (e) => {
      alert('udalit ' + e);
    }

    return {
      events,
      sampleEvent,
      router,
      goToImage: (e) => window.open(e, '_blank'),
      removeItem,
      currentItem,
      previewFullWidth
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
  }
}

.admin-panel__editor__element-inner__wrapper {
  display: flex;
  flex-direction: row;
  gap: 40px;

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

.admin-panel__editor__element-inner__wrapper {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
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
  /* height: 150px; */
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
  position: relative;
}

.zoom--preview {
  position: absolute;
  width: 25px;
  right: 0;
}
</style>
