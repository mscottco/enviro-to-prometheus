import os
import glob
from datetime import datetime
from flask import Flask,request,json,Response
import logging
import sys

if os.getenv('ttl') is None:
    ttl = 15
else:
    ttl = os.getenv('ttl')

log = logging.getLogger('')
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

if os.getenv('DEBUG') == "True":
    log.setLevel(logging.DEBUG)
    logging.info("Debug logging enabled")
else:
    log.setLevel(logging.INFO)

app = Flask(__name__)

def time_diff(timestamp):
    metrics_date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    difference = datetime.now() - metrics_date
    if difference.total_seconds() >= ttl * 60:
        return True
    else:
        return False

@app.route('/metrics')
def metrics():
    metrics_result = '#Enviro Metrics\n'
    for json_file in glob.iglob('readings/*.json'):
        data = json.load(open(json_file))
        logging.debug("JSON contents: {0}".format(data))
        if time_diff(data["timestamp"]):
            for reading in data["readings"]:
                if "moisture" in reading:
                    probe_number = reading.split("_").pop()
                    labels = '{nickname="%s", sensor="%s"}' % (data["nickname"], probe_number)
                    metrics_result += 'enviro_{0}{1} {2}\n'.format("moisture", labels, data["readings"][reading])
                else:
                    labels = '{nickname="%s"}' % data["nickname"]
                    metrics_result += 'enviro_{0}{1} {2}\n'.format(reading, labels, data["readings"][reading])

    return Response(metrics_result, mimetype='text/text')

@app.route('/endpoint',methods=['POST'])
def endpoint():
    data = request.json
    logging.debug("Received JSON: {0}".format(request.json))
    nickname = data["nickname"]
    file_out = "readings/{0}.json".format(nickname)
    with open(file_out, "w") as outfile:
        json.dump(data, outfile)
    return 'success', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)
