import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import CreateFlashCardPage from './pages/CreateFlashCardPage';

// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      CreateFlashCardPage,
    },
    template: '<CreateFlashCardPage/>',
    render: h => h(CreateFlashCardPage)
});