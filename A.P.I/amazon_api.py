from bs4 import BeautifulSoup
import requests
from flask import Flask
app=Flask(__name__)


@app.route("/bazar/<product>")
def item(product):
    htmlContent=getHtmlContent(product)
    soup=BeautifulSoup(htmlContent,'html.parser')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url=list()
    for urls in soup.find_all('a',class_='a-link-normal a-text-normal'):
        url.append('https://www.amazon.in'+urls['href'])
    for urls in soup.find_all('a', class_='a-link-normal s-no-outline'):
        url.append('https://www.amazon.in'+urls['href'])

    products=[]
    for each_url in url:
        print(each_url)
        current_page=BeautifulSoup(requests.get(each_url,headers=headers).text,'html.parser')
        my_dict=dict()

        name=current_page.find('span',class_='a-size-large product-title-word-break')
        if name:
            string=name.text.strip()
            my_dict['name']=string
            print(string)
        
        else:
            continue

        price=current_page.find('span',class_='a-size-medium a-color-price priceBlockBuyingPriceString')
        if price==None:
            price=current_page.find('span',class_='a-size-medium a-color-price priceBlockSalePriceString')
        if price==None:
            price = current_page.find('span', class_='a-size-medium a-color-price priceBlockDealPriceString')
        if price==None:
            my_dict['price']='Currently Unavailable'
        else:
            string2 = price.text.strip()
            print(string2)
            my_dict['price']=string2
        products.append(my_dict)

    return {"products":products}





def getHtmlContent(product):

    headers = {
        'authority': 'www.amazon.in',
        'cache-control': 'max-age=0',
        'rtt': '150',
        'downlink': '10',
        'ect': '4g',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'session-id=262-6377335-6247930; ubid-acbin=261-3806335-9358121; x-acbin=^\\^4LR44R71rRqG6RhWJT4?m7Il2i2GJw6HnJxz^@TiRFIFbbRSawyuBJPJ5pRyf4ztm^\\^; at-acbin=Atza^|IwEBIEoSm1WqTrkPXhwKEpohmoQgmtjxk7-c1BStcDCRFm3A_bBbnPr8_BAj1JSgPJZJm19nYEnQ50f6gUW61MVUtwousBZLRiXs8Up3HLsJG9ty_VwhFLh4nLZ0kSZkcTfs2iTIk4jGpmAtHpPaK26GNTM9qtOeMStvOHXm18nmULR2VgtfsM66myav8-4qLh09KhlDQkpOmf8-4Wo-sguSNkAAxNffu1VC50hQCeSe7xlE6A; sess-at-acbin=^\\^86R6SBy7IlR7yAJ8PsVz+Xl65QOpzCRWhOKXf2PQfe8=^\\^; sst-acbin=Sst1^|PQGxPc8y5rard2jKg_9C19SDCcdliAKA0UbeBWxASe10MIaAbqlWqBUa1IwMfkoDtTJ860qBUPElq0Yu4cz-NCQD4GMbDqEld3NvFaXctUNkHEYt3gEl95gZs0_HXXWgc9JCBh-HGiwb9YwY0NphtakJjWEdCVpQt9Ud1Yh1nIUtbFYPhB1Hslf_mfH0ntwhkGvG_ZBF960ulJrQ1EkJpwhxYddHzq-_6s9-uRgTjW1xnfN8xWpZVScyydwoTZkMVaknc_Nc5r_0d97Ba5N6Vzn2sa1imWJapsrEA9hd3pJqx4E; i18n-prefs=INR; session-token=^\\^0TE92jzCZaCnkkaB8R4fkNdVFWXWkE4/SmsT7wWZ1awg3IhGLI41DgTcoyihTTacCEmhGfxwSZaAc7HSEepWsVQgCFwZiaxs43f19f1EItSWTW9kFma0u0PthLnMrwzsqGglDjhmNOyfge7YeYYCBLSvEwM94ftjP09xjHyhxEntRefj/7IeA1DZosP2xeKr4+p/UKeqGpOsbNewrWYHxA==^\\^; visitCount=32; csm-hit=adb:adblk_no^&t:1600876500766^&tb:s-5378JXFS3PJ3T96Z8B79^|1600876500375; session-id-time=2082758401l',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    params = (
        ('k', product),
        ('ref', 'nb_sb_noss_2'),
    )

    response = requests.get('https://www.amazon.in/s', headers=headers, params=params)
    return response.text
if __name__=='__main__':
    app.run()