import API from "./API";

import Question from "../models/Question";


export default class QuestionAPI extends API {
    async getQuestion(workbookId, questionId) {
        const path = `/api/workbooks/${workbookId}/questions/${questionId}/`;
        const resp = await this.get(path, {});
        const questionData = resp.data.question;
        const question = new Question();
        question.question_id = questionData.question_id;
        question.title = questionData.title;
        question.sentense = questionData.sentense;
        question.chapter = questionData.chapter;
        question.correct_index = questionData.correct_index;
        question.commentary = questionData.commentary;
        question.answers = questionData.answers;
        return question;
    }

    async createQuestion(workbookId, question) {
        const path = `/api/workbooks/${workbookId}/questions/`;
        const {
            title,
            sentense,
            chapter_id,
            correct_index,
            commentary,
        } = question;
        const data = {
            title,
            sentense,
            chapter_id,
            correct_index,
            commentary,
        }
        data['answers'] = [];
        for (var answer of question.answers) {
            const {
                index,
                sentense,
            } = answer;
            const answerForm = {
                index,
                sentense,
            };
            data['answers'].push(answerForm);
        }
        return this.post(path, data);
    }

    async editQuestion(workbookId, question) {
        const path = `/api/workbooks/${workbookId}/questions/${question.question_id}/`;
        const {
            title,
            sentense,
            chapter_id,
            correct_index,
            commentary,
        } = question;
        const data = {
            title,
            sentense,
            chapter_id,
            correct_index,
            commentary,
        }
        data['answers'] = [];
        for (var answer of question.answers) {
            const {
                answer_id,
                index,
                sentense,
            } = answer;
            const answerForm = {
                answer_id,
                index,
                sentense,
            };
            data['answers'].push(answerForm);
        }
        return this.post(path, data);
    }
}