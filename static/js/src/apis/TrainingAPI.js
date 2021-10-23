import API from "./API";


export default class TrainingAPI extends API {
    async createSelection(workbookId, trainingId, question, started_at) {
        var selected_id = undefined;
        for (var answer of question.answers) {
            if (answer.selected) {
                selected_id = answer.answer_id;
            }
        }
        const { question_id } = question;

        const path = `/api/workbooks/${workbookId}/trainings/${trainingId}/selections/`;
        const data = {
            selected_id,
            question_id,
            started_at,
        }
        return this.post(path, data).then(response => response.data.selection);
    }
}