import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import TrainingFlashCardPage from './pages/TrainingFlashCardPage';

// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)

new Vue({
    el: '#main-content',
    components: {
      TrainingFlashCardPage,
    },
    template: '<TrainingFlashCardPage/>',
    render: h => h(TrainingFlashCardPage)
});