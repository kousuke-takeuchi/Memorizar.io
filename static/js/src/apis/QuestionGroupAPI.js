import axios from 'axios';

import API from "./API";
import QuestionGroup from "../models/QuestionGroup";


export default class QuestionGroupAPI extends API {
    async getQuestionGroup(workbookId, questionGroupId) {
        const path = `/api/workbooks/${workbookId}/question_groups/${questionGroupId}/`;
        const resp = await this.get(path, {});
        const questionGroupData = resp.data.question_group;
        const questionGroup = new QuestionGroup();
        return questionGroup;
    }

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

    async createQuestionGroup(workbookId, questionGroup) {
        let path = `/api/workbooks/${workbookId}/question_groups/`;
        let data = {
            'title': questionGroup.title,
            'sentense': questionGroup.sentense,
            'chapter_id': questionGroup.chapter_id,
            'questions': [],
        }
        for (let question of questionGroup.questions) {
            let questionForm = {
                'title': question.title,
                'sentense': question.sentense,
                'chapter_id': question.chapter_id,
                'correct_index': question.correct_index,
                'commentary': question.commentary,
            }
            questionForm['answers'] = [];
            for (var answer of question.answers) {
                let answerForm = {
                    'index': answer.index,
                    'sentense': answer.sentense,
                }
                questionForm['answers'].push(answerForm);
            }
            data['questions'].push(questionForm)
        }
        return this.post(path, data);
    }

    async editQuestionGroup(workbookId, questionGroup) {
        let path = `/api/workbooks/${workbookId}/question_groups/${questionGroup.group_id}`;
        let {
            title,
            sentense,
            chapter_id,
        } = questionGroup;
        let data = {
            title,
            sentense,
            chapter_id,
        }
        data['questions'] = [];
        for (let question of questionGroup.questions) {
            let questionForm = {
                'question_id': question.question_id,
                'title': question.title,
                'sentense': question.sentense,
                'chapter_id': question.chapter_id,
                'correct_index': question.correct_index,
                'commentary': question.commentary,
            }
            questionForm['answers'] = [];
            for (var answer of question.answers) {
                let answerForm = {
                    'answer_id': answer.answer_id,
                    'index': answer.index,
                    'sentense': answer.sentense,
                }
                questionForm['answers'].push(answerForm);
            }
            data['questions'].push(questionForm)
        }
        return this.post(path, data);
    }

    async deleteQuestion(workbookId, question) {
        const path = `/api/workbooks/${workbookId}/questions/${question.question_id}/delete/`;
        return this.post(path);
    }
}