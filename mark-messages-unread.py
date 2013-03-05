"""Accesses to an IMAP mailbox and marks all messages as unseen.
"""

import imaplib
import time
import sys

address = ''
user = ''
password = ''


class MailBox(object):

    def __init__(self, address=address, user=user, password=password):
        self.mail = imaplib.IMAP4_SSL(address)
        self.mail.login(user, password)

    def mark_all_as_unseen(self, folder='inbox'):
        """Marks all messages as unseen and returns the number of messages."""
        self.mail.select(folder)
        typ, data = self.mail.search(None, 'ALL')

        mail_count = 0
        for num in data[0].split():
            self.mail.store(num, '-FLAGS', '\\Seen')
            mail_count += 1
        return mail_count


def main():
    message = ''

    message += 'Started at %s\n' % time.asctime()
    message += 'Connecting to mailbox..\n'
    mailbox = MailBox()

    message += 'Marking all messages as unseen..\n'
    mail_count = mailbox.mark_all_as_unseen('inbox')
    message += '%s mails were marked as unseen.\n' % mail_count

    if mail_count > 0:
        # Redirect stdout -> stderr
        # Cron will send mail if stderr was written.
        sys.stdout = sys.stderr
        print(message)


if __name__ == '__main__':
    main()
