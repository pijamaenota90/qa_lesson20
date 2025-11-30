import allure
import requests
import dotenv
import os
from selene import browser


def add_screenshot(name='screenshot'):
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def add_video(session_id, driver_name):
    if driver_name == 'bstack':
        try:
            bstack_session = requests.get(
                f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
                auth=(os.getenv('USER_NAME'), os.getenv('ACCESS_KEY')),
            )

            if bstack_session.status_code == 200:
                video_url = bstack_session.json().get('automation_session', {}).get('video_url')
                if video_url:
                    allure.attach(
                        f'<video src="{video_url}" width="100%" controls></video>',
                        name='video recording',
                        attachment_type=allure.attachment_type.HTML,
                    )
            else:
                print(f"Не удалось получить видео: {bstack_session.status_code}")

        except Exception as e:
            print(f"Ошибка при получении видео: {e}")