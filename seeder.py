ids = {
    'page_id': 7,
    'article_id': 8,
    'book_id': 1
}


def getPageName(page_title):
    '''
        Converts the given page_title to a valid
        page name
    '''

    replace = {
        '(': '_',
        ')': '_',
        '-': '_',
        ' ': '_',
        '\'': '',
        '\n': '',
        '\t': '',
    }

    page_name = page_title.lower()
    page_name.strip()

    for key in replace:
        page_name = page_name.replace(key, replace[key])

    return page_name


def createArticle():

    article_id = ids['article_id']
    content = 'Coming Soon !!!'
    comments = 0

    query = "INSERT INTO article_content (page_modulecomponentid, article_content, allowComments) VALUES ({}, '{}', {});"

    print(query.format(article_id, content, comments))

    ids['article_id'] += 1
    return article_id


def createBook(articles_in_book=None, template='book_template'):

    book_id = ids['book_id']
    page_parent_id = ids['page_id'] - 1

    if articles_in_book is None:
        articles_in_book = ['Description', 'Rules', 'Venue']

    id_list = []

    for title in articles_in_book:
        page_id = createPage(page_parent_id, title, 'article', template)
        id_list.append(page_id)

    initial = id_list[0]
    id_list = ','.join([str(x) for x in id_list])
    menu_hide = ''

    query = "INSERT INTO book_desc VALUES ({}, {}, '{}', '{}');"
    print(query.format(book_id, initial, id_list, menu_hide))

    ids['book_id'] += 1
    return book_id


def createPage(page_parent_id, page_title, page_module,
               page_template='integriti', page_menu_rank=None):

    page_id = ids['page_id']
    page_name = getPageName(page_title)

    if page_menu_rank is None:
        page_menu_rank = page_id

    ids['page_id'] += 1

    if page_module == 'article':
        page_module_component_id = createArticle()
    elif page_module == 'book':
        page_module_component_id = createBook()

    query = "INSERT INTO pragyanV3_pages (page_id, page_name, page_parentid, page_title, page_module, page_modulecomponentid, page_template, page_menurank) VALUES ({}, '{}', {}, '{}', '{}', {}, '{}', {});"

    print(query.format(page_id, page_name, page_parent_id, page_title, page_module, page_module_component_id, page_template, page_menu_rank))

    return page_id


templates = {
    'events': 'events_template',
    'cluster': 'cluster_template',
    'single_event': 'single_event_template',
}

event_page = createPage(0, 'EVENTS', 'article', templates['events'])

with open('event_list.txt') as events:
    for cluster in events.readlines():
        cluster = cluster.split(',')

        cluster_name = cluster[0]
        event_names = cluster[1:]

        cluster_page = createPage(event_page, cluster_name, 'article', templates['cluster'])

        for event_name in event_names:
            if '[' in event_name:
                start = event_name.index('[')
                end = event_name.index(']')

                sub_cluster_name = event_name[:start]
                sub_cluster_events = event_name[start+1:end].split('$')

                sub_cluster_page = createPage(cluster_page, sub_cluster_name, 'article', templates['cluster'])

                for sub_cluster_event in sub_cluster_events:
                    createPage(sub_cluster_page, sub_cluster_event, 'book', templates['single_event'])

            else:
                createPage(cluster_page, event_name, 'book', templates['single_event'])