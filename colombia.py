#!/usr/bin/env python3
import csv
import logging
import json
import os
import requests
import sys
import urllib
import urllib.request
from time import sleep

SLEEP = 0.5
BASE_URL = "http://comovamos.eokoe.com"

def get_organizations(): 
	"""
	Fetches the list of organizations in the CKAN repository.
	:return: a list of the organizations in the CKAN repository.
	"""
	url = '{base_url}/api/3/action/organization_list'.format(base_url=BASE_URL)
	response = requests.get(url).json()
	organizations = []
	for organization in response['result']:
		organizations.append(organization)
	return organizations


def get_datasets(organization):
	"""
	Fetches the list of datasets of an organization.
	:param organization: the id of the organization for which the datasets will be fetched.
	:return: a list that contains the URLs of the extracted resources.
	"""
	url = '{base_url}/api/3/action/organization_show?id={organization}'.format(base_url=BASE_URL, organization=organization)
	response = requests.get(url).json()
	packages = response['result']['packages']
	datasets = []
	for package in packages:
		datasets.append(package['id'])
	return datasets 

def get_resources(dataset):
	"""
	Fetches the list of resources of each dataset.
	:param dataset: the dataset for which the resources will be fetched.
	:return: a list of urls for each resource
	"""
	url = '{base_url}/api/3/action/package_show?id={dataset}'.format(base_url=BASE_URL, dataset=dataset)
	response = requests.get(url).json()
	r = response['result']['resources']
	resources = []
	for resource in r:
		resources.append(resource['url'])
	return resources

def main():
	logging.basicConfig(level=logging.INFO)
	
	dictionary = {} # Dictionary that aggregates the extracted results.
	urls = []
	organizations = get_organizations()
	
	# CKAN API calls.
	for organization in organizations:
		datasets = get_datasets(organization)
		for dataset in datasets:
			resources = get_resources(dataset)
			for resource in resources:
				urls.append(resource)
				partial_resources = {}
				partial_resources['resources'] = resources
				dictionary[organization] = partial_resources
				sleep(SLEEP)

	l = []

	for key in dictionary:
		resources = dictionary[key]['resources']
		for resource in resources:
			filename = resource.split("/")[-1]
			
			if filename.startswith("indicadores"):
				pass
			elif filename.startswith("diccionario"):
				try:
					response = urllib.request.urlopen(resource)
					reader = csv.reader(response)
					for row in reader:
						print(row)
						id_variable = row[0]
						variable_name = row[1]
						ring_name = row[2]
						theme = row[3]
						d = {}
						d['id'] = id_variable
						d['indicator'] = variable_name
						d['ring'] = ring_name
						d['area'] = theme
						#print(d)
						#l.append(d)
				except:
					pass

if __name__ == '__main__':
	main()


