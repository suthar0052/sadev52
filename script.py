from flask import Flask, render_template
from pandas_datareader import data
from bokeh.plotting import figure, show, output_file
from bokeh.resources import CDN
from bokeh.embed import components
import datetime

app = Flask(__name__)


@app.route('/plot/')
def plot():
    start = datetime.date(2020, 2, 1)
    end = datetime.date(2020, 10, 25)

    # print(start)
    # end = datetime.time(2020,10,25)
    # help(datetime)
    df = data.DataReader('TSLA', 'yahoo', start=start, end=end)

    # df.index[df.Close > df.Open]

    def inc_dec(c, o):
        if c > o:
            return "Increase"
        elif c < o:
            return "Decrease"
        else:
            return "Equal"

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Width"] = 12 * 60 * 60 * 1000
    df["Height"] = abs(df.Open - df.Close)
    df

    f = figure(x_axis_type="datetime", width=1000, height=700, sizing_mode="scale_width")

    f.title.text = "Candlestick Graph"

    f.grid.grid_line_alpha = 0.3

    f.segment(df.index, df.High, df.index, df.Low, line_color="black", line_width=1)

    f.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], df.Width[df.Status == "Increase"],
           df.Height[df.Status == "Increase"], fill_color="green", line_color='black')
    f.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], df.Width[df.Status == "Decrease"],
           df.Height[df.Status == "Decrease"], fill_color="red", line_color='black')
    # help(f.rect)

    script1, div1 = components(f)
    js_files = CDN.js_files[0]
    css_files = CDN.css_files

    # print(components(f))
    # output_file("data.html")
    # show(f)
    return render_template("plot.html", script1=script1, div1=div1, js_files=js_files, css_files=css_files)


@app.route('/')
def home():
    return render_template("/home.html")


@app.route('/about')
def about():
    return render_template("/about.html")


if __name__ == "__main__":
    app.run(debug=True)
