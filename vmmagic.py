from datetime import date
from werkzeug import secure_filename
from flask import Flask, render_template, request
from pandas import pandas

app = Flask(__name__)

@app.route('/')
def vmhome():
    return render_template("vmhome.html")

@app.route('/results/', methods=['POST'])
def results():
    if request.method == "POST":
        try:
            error = "Request error! Make sure you have included all files!"
            today = date.today()
            vm = request.files["vm_file"]
            dfvm = pandas.read_excel(vm)
            mm = request.files["mm_file"]
            dfmm = pandas.read_excel(mm)
            cftpo = request.files["cftpo_file"]
            dfcftpo = pandas.read_excel(cftpo)
            error = "One service number column has not been named SN and has returned a error!"
            moveoutofmm = dfmm[~dfmm.SN.isin(dfvm.SN)]
            moveintomm = dfvm[~dfvm.SN.isin(dfmm.SN)]
            df = dfcftpo[~dfcftpo.SN.isin(dfvm.SN)]
            error = "CFTPO auto-fill error!"
            df.loc[:, "Stop CFTPO"] = today
            df2 = dfvm[~dfvm.SN.isin(dfcftpo.SN)]
            df2.loc[:, "Start CFTPO"] = today
            resultscftpo = df.append(df2)
            resultscftpo = resultscftpo.fillna('')
            return render_template("results.html", moveoout=moveoutofmm.to_html(),
                                   movein=moveintomm.to_html(), cftpo=resultscftpo.to_html())
        except:
            return render_template("error.html", vmerror=error)


if __name__ == '__main__':
    app.run()


