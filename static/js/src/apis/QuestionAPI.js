import API from "./API";


export default class QuestionAPI extends API {
    async getQuestion(workbookId) {
        const path = `/workbooks/${workbookId}/questions/`;
        return this.get(path);
    }

    async createQuestion(workbookId, question) {
        const path = `/workbooks/${workbookId}/questions/`;
        const data = {
            title,
            sentense,
            chapter_id,
            commentary,
        } = question;
        data['answers'] = [];
        for (var answer in question.answerSet.answers) {
            var answerForm = {
                index,
                sentense,
            } = answer;
            data['answers'].push(answerForm);
        }
        return this.post(path, data);
    }
}