import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import EditQuestionPage from './pages/EditQuestionPage';


// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      EditQuestionPage,
    },
    template: '<CreateQuestionPage/>',
    render: h => h(EditQuestionPage)
});