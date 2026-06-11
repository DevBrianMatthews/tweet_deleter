from pyfiglet import figlet_format
from datetime import datetime
from datetime import timezone
from dotenv   import load_dotenv
import click
import os

from main import read_archive, extract_data

from playwright.sync_api import sync_playwright

load_dotenv()

title_tixit = figlet_format("Twixit", font="larry3d")
print(title_tixit)


# ------ PLAYWRIGHT ------------
def login (page, username, password):
    page.goto('https://x.com/')
    page.locator('input[name="username_or_email"]').fill(username)
    page.locator('button[type="submit"]').click()
    page.wait_for_selector('input[name="password"]')
    page.locator('#jf-input-password').fill(password)
    page.locator('#layers').get_by_role('button', name='Continuar').click()
    page.wait_for_url('https://x.com/home')
    click.echo("Login exitoso.")
    
# ------ TWEET DELETER -----------
def delete_tweet(page, tweet_id, username):
    try:
        page.goto(f'https://x.com/{username}/status/{tweet_id}')
        
        tweet_article = page.locator(f'article:has(a[href*="{tweet_id}"])')
        tweet_article.wait_for(state="visible", timeout=5000)
        
        caret_button = tweet_article.locator('button[data-testid="caret"]')
        caret_button.click()
        
        dropdown = page.locator('[data-testid="Dropdown"]')
        dropdown.wait_for(state="visible", timeout=5000)
        
        delete_option = dropdown.get_by_role("menuitem", name="Eliminar", exact=True)
        delete_option.click()
        
        confirm_button = page.locator('[data-testid="confirmationSheetConfirm"]')
        confirm_button.click()

    except Exception as e:
        click.echo(f'Error occurred while trying to process the Tweet {tweet_id}.')

# ------ RETWEET DELETER ------
def delete_retweet(page, tweet_id, username):
    try:
        page.goto(f'https://x.com/{username}/status/{tweet_id}')
        
        unretweet_button = page.locator('button[data-testid="unretweet"]')
        unretweet_button.wait_for(state="visible", timeout=5000)
        unretweet_button.click()
        
        dropdown = page.locator('[data-testid="Dropdown"]')
        dropdown.wait_for(state="visible", timeout=5000)
        
        confirm_button = page.locator('[data-testid="unretweetConfirm"]')
        confirm_button.click()
        
        click.echo(f'Retweet {tweet_id} canceled.')
    except Exception as e:
        click.echo(f'Error occurred while trying to process the Retweet {tweet_id}.')



# ------ ORCHESTRATOR ------------
def run (username, password, data_list, retweet_list, retweet_flag):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless = False,
            slow_mo  = 800,
            args     = ['--disable-blink-features=AutomationControlled']
        )
        page = browser.new_page()
        login(page, username, password)

        if not retweet_flag:
            for tweet in data_list:
                tweet_id = tweet['id']
                delete_tweet(page, tweet_id, username)
        else:
            for tweet in retweet_list:
                tweet_id = tweet['id']
                delete_retweet(page, tweet_id, username)
        
        browser.close()


@click.command()
@click.option(
    '--limit',
    default = None,
    type    = int,
    help    = 'Delete the N most recent tweets'
)

@click.option(
    '--after',
    default = None,
    type    = click.DateTime(formats=['%Y-%m-%d']),
    help    = 'Delete tweets after this date Format: YYYY-MM-DD'
)
@click.option(
    '--before',
    default = None,
    type    = click.DateTime(formats=['%Y-%m-%d']),
    help    = 'Delete tweets before this date Format: YYYY-MM-DD'
)

@click.option(
    '--between',
    default = None,
    nargs   = 2,
    type    = click.DateTime(formats=['%Y-%m-%d']),
    help    = 'Delete tweets between two dates Format: YYYY-MM-DD'
)

@click.option(
    '--retweet',
    is_flag = True,
    default = False,
    help    = 'Delete all retweets'
)

@click.option(
    '--setup',
    is_flag = True,
    help    = 'Configure your X credentials'
)

def twixit(limit: int | None, after: datetime | None, before: datetime | None, between: tuple | None, retweet: bool, setup: bool):

    username = os.getenv('X_USERNAME')
    password = os.getenv('X_PASSWORD')

    if setup or not username or not password:
        username = click.prompt('Enter your username')
        password = click.prompt('Enter your password',
        hide_input=True,
        confirmation_prompt=True
        )

        with open('.env', 'r', encoding='utf-8') as f:
            data = f.read()
            data_list = data.splitlines()
            data_list = [i for i in data_list if 'X_USERNAME' not in i and 'X_PASSWORD' not in i]
            data_list.append(f'X_USERNAME={username}')
            data_list.append(f'X_PASSWORD="{password}"')

        with open('.env', 'w') as f:
            f.write("\n".join(data_list))

        click.echo("✓ Credentials saved. Run 'python twixit.py --help' to see available options.")
        return

    data_list, retweet_list = extract_data(read_archive())
    
    data_list.sort(key=lambda x: x['created'], reverse=True)
    retweet_list.sort(key=lambda x: x['created'], reverse=True)
    
    
    # ------ CONVERT THE TIME ZONE --------
    date_A = None
    date_B = None

    if after is not None:
        after = after.replace(tzinfo=timezone.utc)
    
    if before is not None:
        before = before.replace(tzinfo=timezone.utc)

    if between is not None:
        date_A = between[0].replace(tzinfo=timezone.utc)
        date_B = between[1].replace(tzinfo=timezone.utc)


# ------ FILTER LIMIT -----------
    if limit is not None:
        data_list = data_list[:limit]

# ------ FILTER BEFORE ----------
    if before is not None:
        data_list = [x for x in data_list if x['created'] < before]

# ------ FILTER AFTER ----------
    if after is not None:
        data_list = [x for x in data_list if x['created'] > after]

# ------ FILTER BETWEEN ----------
    if between is not None:
        data_list = [x for x in data_list if date_A <= x['created'] <= date_B]

# ------ FILTER RETWEET ---------
    if not retweet:
        retweet_list = []
    else:
        if after is not None:
            retweet_list = [x for x in retweet_list if x['created'] > after]
        
        if between is not None:
            retweet_list = [x for x in retweet_list if date_A <= x['created'] <= date_B]
        
        if before is not None:
            retweet_list = [x for x in retweet_list if x['created'] < before]
        
        if limit is not None:
            retweet_list = retweet_list[:limit]

    run(username, password, data_list, retweet_list, retweet)

if __name__ == '__main__':
    twixit()