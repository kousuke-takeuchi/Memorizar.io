import axios from 'axios';

import API from "./API";
import Question from "../models/Question";


export default class QuestionAPI extends API {
    async uploadImage(file, width, height, left, top) {
        let path = `/api/workbooks/upload/`;
        let headers = this.getHeader();
        headers['Content-Type'] = 'multipart/form-data';
        let formData = new FormData();
        formData.append('file', file);
        formData.append('width', width);
        formData.append('height', height);
        formData.append('left', left);
        formData.append('top', top);
        return axios.post(path, formData, { headers });
    }

    async getQuestion(workbookId, questionId) {
        let path = `/api/workbooks/${workbookId}/questions/${questionId}/`;
        let resp = await this.get(path, {});
        let questionData = resp.data.question;
        let question = new Question();
        question.question_id = questionData.question_id;
        question.title = questionData.title;
        question.sentense = questionData.sentense;
        question.chapter = questionData.chapter;
        question.image_urls = questionData.image_urls;
        question.correct_index = questionData.correct_index;
        question.commentary = questionData.commentary;
        question.commentary_image_urls = questionData.commentary_image_urls;
        question.answers = questionData.answers;
        return question;
    }

    async createQuestion(workbookId, question) {
        let path = `/api/workbooks/${workbookId}/questions/`;
        let data = {
            'title': question.title,
            'sentense': question.sentense,
            'chapter_id': question.chapter_id,
            'correct_index': question.correct_index,
            'image_urls': question.image_urls,
            'commentary': question.commentary,
            'commentary_image_urls': question.commentary_image_urls,
            'answers': [],
        }
        for (let answer of question.answers) {
            let answerForm = {
                'index': answer.index,
                'sentense': answer.sentense,
            };
            data['answers'].push(answerForm);
        }
        return this.post(path, data);
    }

    async editQuestion(workbookId, question) {
        let path = `/api/workbooks/${workbookId}/questions/${question.question_id}/`;
        let data = {
            'title': question.title,
            'sentense': question.sentense,
            'chapter_id': question.chapter_id,
            'correct_index': question.correct_index,
            'commentary': question.commentary,
            'answers': [],
        };
        for (var answer of question.answers) {
            let answerForm = {
                'answer_id': answer.answer_id,
                'index': answer.index,
                'sentense': answer.sentense,
            };
            data['answers'].push(answerForm);
        }
        return this.post(path, data);
    }

    async deleteQuestion(workbookId, question) {
        let path = `/api/workbooks/${workbookId}/questions/${question.question_id}/delete/`;
        return this.post(path);
    }
}