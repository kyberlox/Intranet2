import { type IUserList } from "@/components/tools/common/SearchList.vue";
export const findValInObject = (searhIn: { fields: { name: string, field: string, value: string | string[] | IUserList[] }[] }, dataToSearch: string) => {
      const res = searhIn.fields.find((e: { field: string }) => e.field == dataToSearch)?.value;
      return res
}
