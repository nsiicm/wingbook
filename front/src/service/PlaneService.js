import api from '@/axios.js';

export const PlaneService = {
    get_planes() {
        return api.get('/planes')
            .then((response) => response.data);
    }
}