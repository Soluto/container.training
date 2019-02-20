#!/usr/bin/env python2
# coding: utf-8
TEMPLATE="""<html>
<head>
  <title>{{ title }}</title>
  <link rel="stylesheet" href="index.css">
  <meta charset="UTF-8">
</head>
<body>
  <div class="main">
    <table>
      <tr><td class="header" colspan="3">{{ title }}</td></tr>

      {% if self_paced %}
        <tr><td class="title" colspan="3">Self-paced tutorials</td></tr>
        {% for item in self_paced %}
          <tr>
            <td>{{ item.title }}</td>
            <td><a class="slides" href="{{ item.slides }}" /></td>
          </tr>
        {% endfor %}
      {% endif %}

      <tr><td class="spacer"></td></tr>

      <tr>
        <td class="footer">
          Maintained by Soluto Engineering (<a href="https://twitter.com/solutoeng">@solutoeng</a>), based on Jérôme Petazzoni (<a href="https://twitter.com/jpetazzo">@jpetazzo</a>) and <a href="https://github.com/soluto/container.training/graphs/contributors">contributors</a> work.
          The original training site is available <a href="http://container.training/">here</a>.
        </td>
      </tr>
    </table>
  </div>
</body>
</html>""".decode("utf-8")

import datetime
import jinja2
import yaml

items = yaml.load(open("index.yaml"))

# Items with a date correspond to scheduled sessions.
# Items without a date correspond to self-paced content.
# The date should be specified as a string (e.g. 2018-11-26).
# It can also be a list of two elements (e.g. [2018-11-26, 2018-11-28]).
# The latter indicates an event spanning multiple dates.
# The first date will be used in the generated page, but the event
# will be considered "current" (and therefore, shown in the list of
# upcoming events) until the second date.

for item in items:
    if "date" in item:
        date = item["date"]
        if type(date) == list:
            date_begin, date_end = date
        else:
            date_begin, date_end = date, date
        suffix = {
                1: "st", 2: "nd", 3: "rd",
                21: "st", 22: "nd", 23: "rd",
                31: "st"}.get(date_begin.day, "th")
        # %e is a non-standard extension (it displays the day, but without a
        # leading zero). If strftime fails with ValueError, try to fall back
        # on %d (which displays the day but with a leading zero when needed).
        try:
            item["prettydate"] = date_begin.strftime("%B %e{}, %Y").format(suffix)
        except ValueError:
            item["prettydate"] = date_begin.strftime("%B %d{}, %Y").format(suffix)
        item["begin"] = date_begin
        item["end"] = date_end

today = datetime.date.today()
coming_soon = [i for i in items if i.get("date") and i["end"] >= today]
coming_soon.sort(key=lambda i: i["begin"])
past_workshops = [i for i in items if i.get("date") and i["end"] < today]
past_workshops.sort(key=lambda i: i["begin"], reverse=True)
self_paced = [i for i in items if not i.get("date")]
recorded_workshops = [i for i in items if i.get("video")]

template = jinja2.Template(TEMPLATE)
with open("index.html", "w") as f:
    f.write(template.render(
    	title="Container Training",
    	coming_soon=coming_soon,
    	past_workshops=past_workshops,
    	self_paced=self_paced,
    	recorded_workshops=recorded_workshops
    	).encode("utf-8"))

with open("past.html", "w") as f:
	f.write(template.render(
		title="Container Training",
		all_past_workshops=past_workshops
		).encode("utf-8"))
