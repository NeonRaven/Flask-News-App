from newsapi import NewsApiClient

def allSources():

    source_result = []

    newsapi = NewsApiClient(api_key = '2c90171bfd444518bc4ebda2e5895ba0')

    sources = newsapi.get_sources()

    source_result.append(sources)

    for source in source_result:
        print(source.status)
    
    return source_result

allSources()