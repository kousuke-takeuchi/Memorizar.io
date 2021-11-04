import Question from './Question';


class QuestionGroup {
    constructor() {
        this.questions = [new Question(4)];
        this.title = null;
        this.sentense = null;
        this.chapter_id = null;
        this.chapter = null;
    }

    addNewQuestion() {
        this.questions.push(new Question(4));
    }
}

export default QuestionGroup;