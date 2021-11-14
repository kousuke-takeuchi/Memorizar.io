import Vue from 'vue';
import VueAxios from 'vue-axios';
import axios from 'axios'

import CreateQuestionPage from './pages/CreateQuestionPage';

import Quill from 'quill'
import VueQuillEditor from 'vue-quill-editor'

import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import MarkdownShortcuts from 'quill-markdown-shortcuts-for-vue-quill-editor'

Quill.register('modules/markdownShortcuts', MarkdownShortcuts)

// https://github.com/axios/axios/issues/632
Vue.use(VueAxios, axios)
Vue.use(VueQuillEditor)

new Vue({
    el: '#main-content',
    components: {
      CreateQuestionPage,
    },
    template: '<CreateQuestionPage/>',
    render: h => h(CreateQuestionPage)
});