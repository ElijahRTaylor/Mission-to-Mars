
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#Import Pandas
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Run all scraping functions and store results in a dictionary
    data = {}
    #def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    data["news_title"] = news_title
    data["featured_image"] =news_p
    

    
    #return news_title, news_p

    # ### Featured Images    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    

    data["featured_image"]=img_url


    #Mars Facts

    try:
    #Convert first table on website into Pandas DataFrame
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
        #Assign  columns and set index to DataFrame
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    # Convert dataframe to html
    data["facts"] = df.to_html(classes="table table-striped")

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    for x in range(4):
    # Browse through each article
        browser.links.find_by_partial_text('Enhanced')[x].click()
    
        html = browser.html
        html_soup = soup(html,'html.parser')
    
        title = html_soup.find('h2', class_='title').text
        img_url = html_soup.find('img', class_='wide-image').get('src')
    
        print(img_url)
        print(title)
    

        mars_hemispheres = {}
        mars_hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        mars_hemispheres['title'] = title
        hemisphere_image_urls.append(mars_hemispheres)

         # Browse back to repeat
        browser.back()
    
    
    data["hemispheres"]=hemisphere_image_urls

   

    #Quit browser
    browser.quit()  
    return data

if __name__ == "__main__":

# If running as script, print scraped data
    print(scrape_all())