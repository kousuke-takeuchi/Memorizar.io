import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import QuestionScanPage from './pages/QuestionScanPage';


// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      QuestionScanPage,
    },
    template: '<QuestionScanPage/>',
    render: h => h(QuestionScanPage)
});