from tasks import collect_links, parse_xml_form


def fetch_and_parse(page_number):
    page_url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber={page_number}'
    link_task = collect_links.delay(page_url)
    links = link_task.get()

    results = []
    for link in links:
        result_task = parse_xml_form.delay(link)
        results.append(result_task)

    print(f'Страница {page_number}')
    for result in results:
        print(result.get())


if __name__ == '__main__':
    for i in range(1,3):
        fetch_and_parse(i)
