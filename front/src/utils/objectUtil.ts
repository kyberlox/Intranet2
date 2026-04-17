export const findValInObject = (searhIn: any, dataToSearch: string) => {
        console.log(searhIn);
      const res = searhIn.fields.find((e: { field: string }) => e.field == dataToSearch)?.value;
      console.log(res)
      return res
}
