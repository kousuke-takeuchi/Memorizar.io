import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import CreateQuestionPage from './pages/CreateQuestionPage';


// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)


new Vue({
    el: '#main-content',
    components: {
      CreateQuestionPage,
    },
    template: '<CreateQuestionPage/>',
    render: h => h(CreateQuestionPage)
});