creds = <get credentials from a ~/.google_credentials>

gc = gspread.login(creds['username'],creds['password'])
worksheet = gc.open(<worksheet name>)
