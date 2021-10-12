import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import CreateQuestionPage from './pages/CreateQuestionPage';

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
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