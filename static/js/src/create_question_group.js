import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import CreateQuestionGroupPage from './pages/CreateQuestionGroupPage';

import Quill from 'quill'
import VueQuillEditor from 'vue-quill-editor'

import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import MarkdownShortcuts from 'quill-markdown-shortcuts-for-vue-quill-editor'
import loading from 'vuejs-loading-screen'

Quill.register('modules/markdownShortcuts', MarkdownShortcuts)

// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)
Vue.use(VueQuillEditor)
Vue.use(loading)

new Vue({
    el: '#main-content',
    components: {
      CreateQuestionGroupPage,
    },
    template: '<CreateQuestionGroupPage/>',
    render: h => h(CreateQuestionGroupPage)
});