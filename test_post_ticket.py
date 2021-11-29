import unittest
import post_ticket


class TestPostTicket(unittest.TestCase):

    def test_fetchTickets(self):
        # for testing wrong URL
        URL = 'https://zccbuff.zendesk.com/api/v2/ticketdfs.json'
        self.assertEqual(post_ticket.fetch_tickets(URL), 404)

    def test_fetchTicketsfromURL(self):
        # for testing if ticket does not exist
        ID = 250
        self.assertEqual(post_ticket.fetch_ticket_from_url(ID), 404)


if __name__ == '__main__':
    unittest.main()
