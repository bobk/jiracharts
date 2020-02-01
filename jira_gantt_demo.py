
#   http://github.com/bobk/jiracharts
#
#   This example code set uses various charting libraries, Python with jira-python and 
#   PowerShell with JiraPS to demonstrate generating useful charts and visualizations from Jira data

from jira import JIRA
import os
import datetime
#   in this program we use both the gantt and plotly libraries as examples
#   all variables for gantt are prefixed with gantt, variables for plotly are prefixed with plotly
import gantt
import plotly.figure_factory as plotlyff

def main():
    
#   get our Jira connection information from env vars    
    server = os.environ['JIRA_SERVER']         # e.g. http://myjiraservername:8080
    project = os.environ['JIRA_PROJECT']       # e.g. MYPROJECTNAME 
    username = os.environ['JIRA_USERNAME']     # your Jira username (username if Jira server, email if Jira Cloud)
    password = os.environ['JIRA_PASSWORD']     # your password - note that for Jira Cloud you will need to use an API token

#   this program is not a demonstration of error-checking, it is a demonstration of charting
#   connect to the server    
    options = { "server" : server }
    jira = JIRA(options, basic_auth=(username, password))

#   search for issues - REPLACE this with your query, the code assumes your query returns only Epics
    issues = jira.search_issues("(project=" + project + ") and (issuetype=Epic) order by created DESC", startAt=0)

    charttitle = "demo of Gantt chart of Jira epics"
    today = datetime.datetime.today()

    ganttchart = gantt.Project(charttitle)
    plotlylist = []
    for issue in issues:
#   REPLACE customfield_xxxxx below with your Jira instance's custom field identifier for Epic Name - get that value from the XML Export issue view on an Epic
        epicname = issue.fields.customfield_10102
#   construct the text for each Gantt bar and get the start/stop dates
#   created and duedate are generally present on every Jira instance - change these fields if you need to
#   e.g. you might also calculate the start date as the creation date of the earliest issue in the epic, and the end date as the end date of the latest issue
        taskname = epicname + " (" + issue.key + ") " + issue.fields.status.name
        startdate = datetime.datetime.strptime(issue.fields.created[0:10], '%Y-%m-%d')
        stopdate = datetime.datetime.strptime(issue.fields.duedate, '%Y-%m-%d')
        
#   add the task to the gantt chart
        gantttask = gantt.Task(name=taskname, start=startdate, stop=stopdate)
        ganttchart.add_task(gantttask)

#   add the task to the plotly chart
        plotlydictentry = dict(Task=taskname, Start=startdate, Finish=stopdate)
        plotlylist.append(plotlydictentry)

#   write the gantt chart to a file
    ganttchart.make_svg_for_tasks(filename="ganttchart.svg", today=today, scale=gantt.DRAW_WITH_WEEKLY_SCALE)

#   the plotly chart will pop up in the browser
    plotlyfig = plotlyff.create_gantt(plotlylist, title=charttitle, showgrid_x=True, show_hover_fill=True)
    plotlyfig.show()
       
if __name__== "__main__" :
    main()
