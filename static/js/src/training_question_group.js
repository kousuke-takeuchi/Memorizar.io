import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import TrainingQuestionPage from './pages/TrainingQuestionPage';


// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      TrainingQuestionPage,
    },
    template: '<TrainingQuestionPage/>',
    render: h => h(TrainingQuestionPage)
});