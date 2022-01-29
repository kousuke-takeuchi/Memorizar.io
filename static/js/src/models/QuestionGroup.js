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
        let question = new Question(4);
        let lastQuestion = this.questions[this.questions.length - 1];
        for (let index in question.answers) {
            question.answers[index].sentense = lastQuestion.answers[index].sentense;
        }
        this.questions.push(question);
    }

    setChapter(chapterId) {
        this.chapter_id = chapterId;
        for (let question of this.questions) {
            question.chapter_id = chapterId;
        }
    }
}

export default QuestionGroup;