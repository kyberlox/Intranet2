export default class Api {
    static async get(url: string) {
        const response = await fetch(`${VITE_API_URL}/${url}`);
        return await response.json();
    }
}
const VITE_API_URL = import.meta.env.VITE_API_URL;