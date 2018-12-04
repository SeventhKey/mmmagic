from flask import Flask, render_template, request
from pandas import pandas
from datetime import date

app = Flask(__name__)


@app.route('/')
def vmhome():
    return render_template("vmhome.html")

@app.route('/results/', methods=['POST'])
def results():
    try:
        if request.method == "POST":
            today = date.today()
            vm = request.files["vm_file"]
            mm = request.files["mm_file"]
            cftpo = request.files["cftpo_file"]
            dfvm = pandas.read_excel(vm)
            dfmm = pandas.read_excel(mm)
            dfcftpo = pandas.read_excel(cftpo)
            moveoutofmm = dfmm[~dfmm.SN.isin(dfvm.SN)]
            moveintomm = dfvm[~dfvm.SN.isin(dfmm.SN)]
            df = dfcftpo[~dfcftpo.SN.isin(dfvm.SN)]
            df.loc[:, "Stop CFTPO"] = today
            df2 = dfvm[~dfvm.SN.isin(dfcftpo.SN)]
            df2.loc[:, "Start CFTPO"] = today
            resultscftpo = df.append(df2)
            resultscftpo = resultscftpo.fillna('')
            return render_template("results.html", moveoout=moveoutofmm.to_html(),
                                   movein=moveintomm.to_html(), cftpo=resultscftpo.to_html())
        else:
            return render_template('vmhome.html')
    except:
        return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
