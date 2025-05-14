import type { IBlog } from "@/interfaces/IEntities";
import type { IActualNews, ICareSlide } from "@/interfaces/IEntities";

interface IIndirectDataPlug {
    [key: string]: any;
}

export const getProperty = (object: IActualNews | ICareSlide | IBlog, field: string) => {

    if (!object.indirect_data) return;

    const indirectData = object.indirect_data as IIndirectDataPlug;

    console.log(indirectData && indirectData[field] && indirectData[field][0]);
    if (indirectData && indirectData[field] && indirectData[field][0]) {

        return indirectData[field][0];
    }
}