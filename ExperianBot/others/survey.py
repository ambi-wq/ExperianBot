from flask import Flask, request, redirect,render_template,url_for
from flask import Flask
from model.MySQLHelper import insertquery, create_query

app = Flask(__name__)

@app.route("/showSurveyData", methods=["POST", "GET"])
def show_survey_data():
    user = '1001'
    if request.method == "POST":
        survey_title = request.form['surveytitle']
        print(survey_title)
        query = "select survey_id from survey where title = '" + survey_title + "'"
        output = create_query(query)
        survey_id = output[0][0]
        print("survey id ========= ", survey_id)

        query = "select survey_submit_details.emp_id,survey_submit_details.emp_name,survey_submit_details.question_id," \
                "cast(survey_submit_details.submitted_date as date),survey_submit_details.answer,survey_details.question " \
                "from survey_submit_details INNER JOIN survey_details ON survey_submit_details.question_id = survey_details.question_id " \
                "where survey_submit_details.survey_id = '" + str(survey_id) + "' order by survey_submit_details.emp_id"
        output = create_query(query)
        details = list(output)

        return render_template('survey_details.html',details=details)
    return render_template('survey_details.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=6010, threaded=True)

