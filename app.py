import os
import random
from flask import *
from peewee import *
from setting import SetDb
from test_info import *

app = Flask(__name__, static_folder='./resource')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
SetDb.set_db(app.debug)

from model import *
test_info=TestInfo()


@app.route("/", methods=["GET", "POST"])
def top():
    if request.method == "POST":
        start_id = request.form.get('start_btn')
        change_mode_id = request.form.get('chenge_mode')
        section_list = []
        if start_id:
            for i in range(1,21):
                request_str = "section_"+str(i)
                request_result = request.form.get(request_str)
                if request_result:
                    section_list.append(i)
            test_info.set_sec(section_list)
            return redirect(url_for('test'))
        if change_mode_id:
            test_info.change_mode()
    db.connect()
    return render_template(
        'index.html',
        dbStr = SetDb.DB ,
        test_mode = test_info.get_mode()
        )

@app.route("/registration", methods=["GET", "POST"])
def registration():
    error_flag_dict = {}
    input_val_dict = {}
    if request.method == "POST":
        print(request.form)
        input_val_dict['keyword'] = keyword = request.form['keyword']
        input_val_dict['explain'] = explain = request.form['explain']
        input_val_dict['chapter'] = chapter = request.form['chapter']
        input_val_dict['comment'] = comment = request.form['comment']
        if not keyword:
            error_flag_dict['keyword'] = "keyword:error"
        if not explain:
            error_flag_dict['explain'] = "explain:error"
        if not chapter or not chapter.isdecimal():
            error_flag_dict['chapter'] = "chapter:error"
        if 0 < len(error_flag_dict):
            return render_template(
                'registration.html',
                error_flag = error_flag_dict,
                input_val_dict = input_val_dict
                )
        Question.create(
            keyword = keyword,
            explain = explain,
            chapter = int(chapter),
            number_of_question = 0,
            the_number_of_correct_answers = 0,
            comment = comment
        )
        return render_template('complete.html')
    return render_template(
        'registration.html',
        error_flag = error_flag_dict,
        input_val_dict = input_val_dict
        )

@app.route("/q_list", methods=["GET", "POST"])
def q_list():
    questions = Question
    update_form = request.form.get('update')
    if update_form != None:
        # print(f"update_form : {request.form},  {request.form.get('explain')}")
        q = Question.update({Question.keyword:request.form.get('keyword')}).where(Question.id==int(update_form))
        q.execute()
        q = Question.update({Question.explain:request.form.get('explain')}).where(Question.id==int(update_form))
        q.execute()
        chapter_val = request.form.get('chapter')
        if chapter_val != 'default':
            q = Question.update({Question.chapter:chapter_val}).where(Question.id==int(update_form))
            q.execute()
        q = Question.update({Question.comment:request.form.get('comment')}).where(Question.id==int(update_form))
        q.execute()

    edit_id = request.form.get('edit')
    delete_id = request.form.get('delete')
    count_reset_id = request.form.get('count_reset')
    if request.method == "POST":
        # ---- 編集 ----
        if edit_id != None:
            target_q = questions.get_by_id(edit_id)
            return render_template(
            'edit.html',
            id = edit_id,
            question = target_q
            )
        # ---- 削除 ----
        if delete_id != None:
            questions.delete_by_id(delete_id)
        # ---- 回数リセット ----
        if count_reset_id != None:
            questions.delete_by_id(delete_id)
            q = (Question.update({Question.number_of_question:00})
            .where(Question.id==count_reset_id))
            q.execute()
            q = (Question.update({Question.the_number_of_correct_answers:00})
            .where(Question.id==count_reset_id))
            q.execute()
    return render_template(
        'q_list.html',
        questions = questions
        )

@app.route("/test", methods=["GET", "POST"])
def test():
    questions = Question
    id_list = []

    # チェックボックスのチェックに応じて章を絞る
    for capter in test_info.get_sec():
        for q in Question.get_specific_chapter(capter):
            id_list.append(q.id)
    if len(id_list) == 0:
        for q in questions:
            id_list.append(q.id)

    # DBからランダムな問題を持ってきている
    minimum_q_count = -1
    minimum_q_id = -1
    # 出題回数が少ない順に表示する
    for id in id_list:
        num_of_q =  questions.get_by_id(id).number_of_question
        if minimum_q_count == -1 or num_of_q < minimum_q_count:
            minimum_q_count = num_of_q
            minimum_q_id = id
    # random_num = random.randint(0, len(id_list) - 1)
    if minimum_q_id == -1:
        abort(404)
    target = questions.get_by_id(minimum_q_id)
    current_count = target.number_of_question
    q = (Question.update({Question.number_of_question:current_count + 1})
         .where(Question.id==int(target.id)))
    q.execute()
    if request.method == "POST":
        correct_id = request.form.get('correct')
        if correct_id:
            correct_model = questions.get_by_id(int(correct_id))
            correct_count = correct_model.the_number_of_correct_answers
            q = (Question.update({Question.the_number_of_correct_answers:correct_count + 1})
            .where(Question.id==int(correct_model.id)))
            q.execute()
            print("target"+str(correct_id))
    return render_template(
    'test.html',
    target = target,
    current_selected_chapter = str(test_info.get_sec()),
    test_mode = test_info.get_mode()
    )

@app.route("/download", methods=["GET"])
def download_api():
    filepath = "./db_product.db"
    filename = os.path.basename(filepath)
    return send_file(filepath, as_attachment=True,
                     mimetype='text/plain')

if __name__ == "__main__":
    app.run()