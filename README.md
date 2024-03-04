PARSER FOR OLX.KZ
----------------------------------------------------------------------

1. You need create your account on ZenRows.com
2. After get your personal API to work with ProxyRotator
3. Buy Develepor or other subscripition for you
4. Install Requirements.txt by command: pip install -r requirements.txt
5. Start main.py in console by command: python main.py
   
-----------------------------------------------------------------------

This parser first of all gather offer's ids and offer's url. \n
After gather information, parser use Selenium in headless mode to get username and location. 
And last part of parsing work, it use OLX API to get phone number.
For this process parser use requests library, ZenRows API and OLX Authorization Header, that is Bearer Token.
Every 30 requests parser update Bearer Token, because OLX have limits on one Bearer Token. 
Parser use ProxyRotator to bypass all security things on website.
