import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import TrainingAnswerPage from './pages/TrainingAnswerPage';


// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      TrainingAnswerPage,
    },
    template: '<TrainingAnswerPage/>',
    render: h => h(TrainingAnswerPage)
});