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
	error = None
	
	if request.files.get('vm_file', None):
		return render_template("error.html", vmerror="Request error! Make sure you have included all files!")
	elif request.files.get('mm_file', None):
		return render_template("error.html", vmerror="Request error! Make sure you have included all files!")
	elif request.files.get('cftpo_file', None):
		return render_template("error.html", vmerror="Request error! Make sure you have included all files!")
	
	try:
		dfvm = pandas.read_excel(request.files["vm_file"])
		dfmm = pandas.read_excel(request.files["mm_file"])
		dfcftpo = pandas.read_excel(request.files["cftpo_file"])
	except:
		error = "Inoperable File. Please confirm you have the correct file."
		
	try:
		moveoutofmm = dfmm[~dfmm.SN.isin(dfvm.SN)]
		moveintomm = dfvm[~dfvm.SN.isin(dfmm.SN)]
		df = dfcftpo[~dfcftpo.SN.isin(dfvm.SN)]
	except:
		error = "One service number column has not been named SN and has returned a error!"
		
	try:
		df.loc[:, "Stop CFTPO"] = date.today() # Don't need to define a variable for this since it's an inexpensive/optimized call used only twice
		df2 = dfvm[~dfvm.SN.isin(dfcftpo.SN)]
		df2.loc[:, "Start CFTPO"] = date.today()  # Don't need to define a variable for this since it's an inexpensive/optimized call used only twice
		resultscftpo = df.append(df2)
		resultscftpo = resultscftpo.fillna('')
	except:
		error = "CFTPO auto-fill error!"
	
	
	if error is None:
		return render_template("results.html", moveoout=moveoutofmm.to_html(),
							   movein=moveintomm.to_html(), cftpo=resultscftpo.to_html())
	else:
		return render_template("error.html", vmerror=error)

		
if __name__ == '__main__':
    app.run()

