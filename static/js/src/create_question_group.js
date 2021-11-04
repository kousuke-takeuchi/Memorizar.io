import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import CreateQuestionGroupPage from './pages/CreateQuestionGroupPage';


// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      CreateQuestionGroupPage,
    },
    template: '<CreateQuestionGroupPage/>',
    render: h => h(CreateQuestionGroupPage)
});