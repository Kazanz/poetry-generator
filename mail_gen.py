import json
import random
from poem import bnfDictionary


def render_message(template, ctx):
    """Takes the template and renders the message."""
    with open(template, 'r') as f:
        msg = str(f.read())
        for k, v in ctx.iteritems():
            tag = "{{ " + k + " }}"
            msg = msg.replace(tag, v)
        return msg


def generate_random_message(ctx):
    """Randomly chooses the message to use for the email."""
    # TODO make this find the number of files in the dir for the randInt
    msg_num = random.randint(0, 1)
    template = "msgs/msg{}.txt".format(msg_num)
    return render_message(template, ctx)


def send_emails():
    """Send random poem to all emails on the email list with random email
    template."""
    with open('emails.json', 'r') as f:
        emails = json.loads(f.read())
    for title, email in emails.iteritems():
        bnf = bnfDictionary('poems.bnf')
        poem = bnf.generatePretty('<poem>')
        ctx = {
            'title': title,
            'poem': poem,
        }
        msg = generate_random_message(ctx)
        # TODO Connect and send via IMAP from Gmail.
        print "Send to {}".format(email)
        print msg


if __name__ == "__main__":
    send_emails()
