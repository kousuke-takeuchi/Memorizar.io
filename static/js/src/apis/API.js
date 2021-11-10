import axios from 'axios';


export default class API {
    constructor(token) {
        this.token = token;
    }

    getHeader() {
        return {
            'Authorization': `Token ${this.token}`
        };
    }

    async get(path, params = {}) {
        const headers = this.getHeader();
        return axios({
            method: 'get',
            url: path,
            data: params,
            headers: headers,
        });
        return axios.get(path, params, { headers });
    }

    async post(path, data = {}) {
        const headers = this.getHeader();
        return axios.post(path, data, { headers });
    }
}