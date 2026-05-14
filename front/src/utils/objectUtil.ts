export const findValInObject = (searhIn: any, dataToSearch: string) => {
      const res = searhIn.fields.find((e: { field: string }) => e.field == dataToSearch)?.value;
      return res
}
