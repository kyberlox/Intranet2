import { type Ref, ref } from "vue";
import { allowedTypes } from '@/assets/static/uploadAllowedTypes';
import { type IFileToUpload } from "@/interfaces/entities/IAdmin";

export const useFileUtil = (uploadType: 'img' | 'docs' | 'videoNative') => {
    const allowedType: Ref<string[]> = ref(allowedTypes[uploadType]);

    const validateFile = (allowedType: Ref<string[]>, file: File) => {
        if (!allowedType.value.includes(file.type)) {
            return 'Неподдерживаемый формат файла';
        }
        return true;
    }


    const handleFileSelect = (event: Event) => {
        const target = event.target as HTMLInputElement;
        if (target.files) {
            processFiles(target.files);
        }
    };

    const processFiles = (files: FileList | File[]): string | IFileToUpload => {
        const fileArray = Array.from(files);
        const fileResult: IFileToUpload[] = [];
        fileArray.forEach(file => {
            const validateResult = validateFile(allowedType, file);
            if (validateResult == true) {
                const videoFile: IFileToUpload = {
                    name: file.name,
                    size: file.size,
                    url: URL.createObjectURL(file),
                    file: file
                };
                fileResult.push(videoFile);
            }
        });
        return fileResult[0]
    };

    return {
        validateFile,
        handleFileSelect,
        processFiles
    }
}