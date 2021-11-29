import sys

from flask import Flask, render_template, abort
import post_ticket
import math

app = Flask(__name__)

get_ticket = post_ticket

ALL_TICKETS = 'https://zccbuff.zendesk.com/api/v2/tickets.json'
ROWS_PER_PAGE = 25
CURRENT_PAGE = 0

data = get_ticket.fetch_tickets(ALL_TICKETS)
if data == 401:
    print('Authentication error. Please check username or password')
    sys.exit()
else:
    TOTAL_PAGES = math.ceil(len(data) / ROWS_PER_PAGE)


# For handling common http errors

# API/Web server is not available
@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html'), 503


# Authentication error
@app.errorhandler(401)
def authentication_error(e):
    return render_template('401.html'), 401


# Website not able to find the request
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal server error
@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


# Default page which will display first 25 pages

@app.route('/', methods=['GET', 'POST'])
def displayTicket():
    global ROWS_PER_PAGE, CURRENT_PAGE
    global TOTAL_PAGES
    global data
    CURRENT_PAGE = 0
    page_data = data[0:ROWS_PER_PAGE]
    if len(page_data) == 0:
        abort(404)
    if data == 503:
        abort(503)
    return render_template('display_ticket.html', data=page_data, current_page=CURRENT_PAGE,
                           total_pages=TOTAL_PAGES)


# Next pages till all tickets are displayed. Each page shows 25 tickets

@app.route('/<current_page>', methods=['GET', 'POST'])
def displayTicket_withPagination(current_page):
    global CURRENT_PAGE, ROWS_PER_PAGE
    global TOTAL_PAGES
    global data
    CURRENT_PAGE = int(current_page)
    page_data = data[(CURRENT_PAGE * ROWS_PER_PAGE):(CURRENT_PAGE + 1) * ROWS_PER_PAGE]
    if len(page_data) == 0:
        abort(404)
    if data == 503:
        abort(503)
    return render_template('display_ticket.html', data=page_data, current_page=CURRENT_PAGE, total_pages=TOTAL_PAGES)


# For viewing individual tickets

@app.route('/individualticket/<ticketId>', methods=['GET', 'POST'])
def displayIndividualTicket(ticketId):
    ticket = get_ticket.fetch_ticket_from_url(ticketId)
    if ticket == 503:
        abort(503)
    return render_template('singleticket.html', data=ticket)


if __name__ == '__main__':
    app.run()
