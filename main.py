from flask import Flask, request, render_template, redirect, url_for
from sql_requests import *

app = Flask(__name__)


@app.route('/', methods=['post', 'get'])
def index():
    companies_list = []
    first_date = first_transaction()
    last_date = last_transaction()
    number_of_tranz = count_transactions()
    if request.method == 'POST':
        if request.form['button'] == 'getcompanylist':
            companies_list = get_all_companies()
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
        'number_of_tranz': number_of_tranz
        }
    return render_template('index.html', **template_context)

@app.route('/report/')
def report():
    company_id = request.args['company_id']
    #company_id = 4 # временно
    first_date = request.args['first_date']
    last_date = request.args['last_date']
    print ('report:', company_id, first_date, type(first_date))

    phones_mssql_list = get_mssql_phones(company_id,
                                         first_date.replace('-', ''),
                                         last_date.replace('-', ''))
    print(phones_mssql_list)
    top_phones_list = phones_mssql_list[:5]
    bottom_phones_list = phones_mssql_list[-5:]
    template_context = {
        'companyid': company_id,
        'firstdate': first_date,
        'lastdate': last_date,
        'top_phones_list': top_phones_list,
        'bottom_phones_list': bottom_phones_list,
        'len_of_phones_list': len(phones_mssql_list)
        }
    return render_template('report.html', **template_context)

if __name__ == '__main__':
    app.run(debug=True)
