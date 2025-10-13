import { type Ref, ref } from "vue";
import { allowedTypes } from '@/assets/static/uploadAllowedTypes';
import { type IFileToUpload } from "@/interfaces/IEntities";

export const useFileUtil = (uploadType: 'images' | 'documentation' | 'videos_native') => {
    const allowedType: Ref<string[]> = ref(allowedTypes[uploadType]);

    const validateFile = (allowedType: Ref<string[]>, file: File) => {
        if (!allowedType.value.includes(file.type)) {
            return alert('Неподдерживаемый формат файла');
        }
        return true;
    }

    const handleFileSelect = (event: Event) => {

        const target = event.target as HTMLInputElement;
        if (target.files) {
            return processFiles(target.files);
        }
    };

    const processFiles = (files: FileList | File[]): string | IFileToUpload[] | IFileToUpload => {

        const fileArray = Array.from(files);
        const fileResult: IFileToUpload[] = [];
        fileArray.forEach(file => {
            const validateResult = validateFile(allowedType, file);

            if (validateResult == true) {

                const newFile: IFileToUpload = {
                    name: file.name,
                    size: file.size,
                    url: URL.createObjectURL(file),
                    file: file
                };
                fileResult.push(newFile);
            }
        });

        return fileResult
    };

    return {
        validateFile,
        handleFileSelect,
        processFiles
    }
}