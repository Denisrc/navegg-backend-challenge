#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navegg.settings')

import django
django.setup()

import csv
from sites.models import Sites, SiteCategory, SiteURL 

def create_model(row):
    print(f'Create site {row[0]} with status {row[3]}:')
    print(f'\tURLS: {row[1]}')
    print(f'\tCategories: {row[2]}')

    urls = row[1].split(';')
    categories = row[2].split(';')

    site = Sites()
    site.name = row[0]
    site.active = True if row[3] == 'active' else False
    site.save()

    url_objects = create_urls(urls)
    category_objects = create_categories(categories)

    for url_object in url_objects:
        site.url.add(url_object)
    for category_object in category_objects:
        site.category.add(category_object)

    site.save()
        
def create_categories(categories):
    sites_categories = []
    for category in categories:
        if not SiteCategory.objects.filter(description=category).exists():
            site_category = SiteCategory.objects.create(description=category)
        else:
            site_category = SiteCategory.objects.get(description=category)
        sites_categories.append(site_category)
    return sites_categories

def create_urls(urls):
    sites_url = []
    for url in urls:
        if not SiteURL.objects.filter(description=url).exists():
            site_url = SiteURL.objects.create(description=url)
        else:
            site_url = SiteURL.objects.get(description=url)
        sites_url.append(site_url)
    return sites_url


def main():
    print('Populating the database...')
    with open('../sites.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                create_model(row)
            line_count += 1
    print('Polutation done')

if __name__ == '__main__':
    main()