import os
import requests
from threading import Thread

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

NOTIFY_API_SECRET = os.environ.get("NOTIFY_API_SECRET")
NEXT_PUBLIC_PROJECT_ID = os.environ.get("NEXT_PUBLIC_PROJECT_ID")


class Notifier:
    url = f"https://notify.walletconnect.com/{NEXT_PUBLIC_PROJECT_ID}/notify"
    headers = {"Authorization": f"Bearer {NOTIFY_API_SECRET}"}
    notification_body = {
        "type": "2ad0439a-0f41-40e4-900e-f4af8c06ade7",
        "title": "Donation",
        "body": "Donation received of {} weth",
        "icon": "https://app.pulsar.finance/pulsar-logo-magenta-default.svg",
        "url": "https://warakaton.vercel.app/",
    }

    @classmethod
    def queue_notification(cls, address: str, amount: float):
        if not NOTIFY_API_SECRET:
            return print("Missing NOTIFY_API_SECRET on .env")
        if not NEXT_PUBLIC_PROJECT_ID:
            return print("Missing NEXT_PUBLIC_PROJECT_ID on .env")
        Thread(target=cls.notify, args=(address, amount), daemon=True).start()

    @classmethod
    def notify(cls, address: str, amount: float):
        notification_body = dict(cls.notification_body)
        notification_body["body"] = notification_body["body"].format(amount)
        body = {
            "notification": notification_body,
            "accounts": [f"eip155:1:{address}"],
        }
        resp = requests.post(cls.url, headers=cls.headers, json=body)
        print(f"Notify response => {resp.status_code}: {resp.json()}")
        return
