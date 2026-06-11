import { type IUserList } from "@/components/tools/common/SearchList.vue";

export type searchIn = { fields: { name: string, field: string, value: string | string[] | IUserList[] }[] }
export const findValInObject = (searhIn: searchIn, dataToSearch: string) => {
      const res = searhIn.fields.find((e: { field: string }) => e.field == dataToSearch)?.value;
      if (!res) return

      return (dataToSearch == 'users' && !Array.isArray(res)) ? [res] : res
}
