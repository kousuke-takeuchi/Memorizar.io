import axios from 'axios';


export default class API {
    async get(path, params = {}) {
        const headers = this.getHeader("get", path);
        return axios.get(path, params, { headers });
    }

    async post(path, data = {}) {
        const headers = this.getHeader("post", path);
        return axios.post(path, data, { headers });
    }
}