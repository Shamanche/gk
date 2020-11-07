from flask import Flask, request, render_template, redirect, url_for, send_file
from sql_requests import *
import datetime

app = Flask(__name__)

#преобразует строку c датой вида '%Y-%m-%d' к строке '%Y-%d-%m'
def convert_date(string):
    date = datetime.datetime.strptime(string, '%Y-%m-%d')
    print('date: ', date)
    return date.strftime('%Y-%d-%m')

def make_file(data, filename='testfile1'):
    full_name = (filename + '_'
                        + datetime.datetime.now().strftime('%Y-%m-%d') + '.csv')
    with open (full_name, 'w') as f:
        for i in data:
            f.write(i+'\n')
    return full_name

@app.route('/', methods=['post', 'get'])
def index():
    filename1 = 'file1.csv'
    try:
        conn = mssql_connect()
    except pyodbc.OperationalError as e:
        return render_template('error.html', error_message=e)
    companies_list = []
    first_date = first_transaction(conn)
    last_date = last_transaction(conn)
    number_of_tranz = count_transactions(conn)
    if request.method == 'POST':
        if request.form['button'] == 'getcompanylist':
            companies_list = get_all_companies(conn)
        if request.form['button'] == 'getdata':
            company_id = request.form['companyid']
            first_date = request.form['firstdate']
            last_date = request.form['lastdate']
            print('Данные при получении из формы: ', first_date, type(first_date))
            return redirect(url_for('report',
                                        company_id=company_id,
                                        first_date=first_date,
                                        last_date=last_date))
    template_context = {
        'firstdate': first_date,
        'lastdate': last_date,
        'companies_list': companies_list,
        'number_of_tranz': number_of_tranz,
        'filename1': filename1
        }
    return render_template('index.html', **template_context)

@app.route('/report/')
def report():
    try:
        conn = mssql_connect()
    except pyodbc.OperationalError as e:
        return render_template('error.html', error_message=e)
    company_id = request.args['company_id']
    #company_id = 4 # временно
    first_date = request.args['first_date']
    last_date = request.args['last_date']
    print ('report:', company_id, first_date, type(first_date))

    phones_mssql_list = get_mssql_phones(conn,
                                        company_id,
                                        convert_date(first_date),
                                        convert_date(last_date))
    #print(phones_mssql_list)
    try:
        conn = mysql_connect()
    except pymysql.err.OperationalError as e:
        return render_template('error.html', error_message=e)

    phones_mysql_list = get_mysql_phones(conn)
    mssql_phones_set = set(i[0][1:] for i in phones_mssql_list)
    mysql_phones_set = set(i[0] for i in phones_mysql_list)
    result = mssql_phones_set & mysql_phones_set

    mssql_filename = make_file(mssql_phones_set, 'Телефоны клиентов компании')
    mysql_filename = make_file(mysql_phones_set, 'Телефоный всех клиентов')
    result_filename = make_file(result, 'Результат')

    template_context = {
        'companyid': company_id,
        'firstdate': first_date,
        'lastdate': last_date,
        'number_mssql_phones': len(phones_mssql_list),
        'number_mysql_phones': len(phones_mysql_list),
        'number_result': len(result),
        'mssql_filename': mssql_filename,
        'mysql_filename': mysql_filename,
        'result_filename': result_filename
        }
    return render_template('report.html', **template_context)

@app.route('/files/<filename>')
def files(filename):
    pass
##    full_filename = 'files\\' + filename
##    print('Full filename', full_filename)
##    print('URL FOR ', url_for('files', filename=filename))
##    return send_file(full_filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
