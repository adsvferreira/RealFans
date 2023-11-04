from realfans_api.data.models import *

def parse_user_added_event(event):
    event_args = event.args
    return UserAdded(event_args.userAddress, event_args.userHandle)

def parse_donation_event(event):
    event_args = event.args
    return Donation(event_args.donator, event_args.receiverTwitterHandle, event_args.giftURI, event_args.ethValue, False)

def parse_redemption_event(event):
    event_args = event.args
    return Redemption(event_args.receiver, event_args.receiverTwitterHandle, event_args.giftURI, event_args.ethValue)

def parse_badge_minted_event(event):
    event_args = event.args
    return BadgeMinted(event_args.receiver, event_args.badgeURI)