import praw

app_id = 'xnUqkuJXt88zkw'
app_secret = 'RoGQIOCd2VDokb4BHLLW_alNmvQ'
app_uri = 'https://127.0.0.1:65010/authorize_callback'
app_ua = 'Looks for a matching comment to a word of the day and congratulates them.'
app_scopes = 'read submit'
app_account_code = 'FxwcjaBUGwlwrjqKo9mTUXpwJkk'
app_refresh = '21933210-DOneV3wnDpiDk6mQC6LmnfoKIA0'

def login():
	r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r