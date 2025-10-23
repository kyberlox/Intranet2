export const findValInObject = (searhIn: any, dataToSearch: string) => {
      return searhIn.fields.find((e: { field: string }) => e.field == dataToSearch)?.value;
}