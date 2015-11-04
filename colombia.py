#!/usr/bin/env python3
import csv
import io
import json
import logging
import os
import pandas as pd
import requests
import sys
import urllib
import urllib.request
from time import sleep

__author__ = "Cívica Digital"
__version__ = "1.0"

SLEEP = 0.1
BASE_URL = "http://comovamos.eokoe.com"

def get_organizations(): 
	"""
	Fetches the list of organizations in the CKAN repository.
	:return: a list of the organizations in the CKAN repository.
	"""
	url = '{base_url}/api/3/action/organization_list'.format(base_url=BASE_URL)
	try:
		response = requests.get(url).json()
	except:
		print("Organization list not found", file=stderr)
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
	try:
		response = requests.get(url).json()
	except:
		print("Organization not found.", file=stderr)
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
	try:
		response = requests.get(url).json()
	except:
		print("Package not found.", file=stderr)
	r = response['result']['resources']
	resources = []
	for resource in r:
		resources.append(resource['url'])
	return resources

def get_indicators(url, indicator_id):
	"""
	Fetches the values of a variables across different years.
	:param url: the URL of the indicator file.
	:param indicator_id: the id of the indicator (variable).
	:return: a dict object in the form {years:values}
	"""
	response = urllib.request.urlopen(url)
	df = pd.read_csv(response) # Should use skiprows=X
	header_names = list(df.columns.values)
	header_names.remove('LOCALIDAD')
	header_names.remove('CIUDAD')
	header_names.remove('ANIO')
	years = list(df['ANIO'].apply(str))
	d = {}	
	if indicator_id in header_names:
		values = list(df[indicator_id])
		d = dict(zip(years, values))
	return d

def main():
	logging.basicConfig(level=logging.INFO)
	
	dictionary = {} # Dictionary that aggregates the extracted results.
	# urls = []
	organizations = get_organizations()
	
	# CKAN API calls.
	for organization in organizations:
		datasets = get_datasets(organization=organization)
		for dataset in datasets:
			resources = get_resources(dataset=dataset)
			for resource in resources:
				# urls.append(resource)
				partial_resources = {}
				partial_resources['resources'] = resources
				dictionary[organization] = partial_resources
				sleep(SLEEP)

	# The final dictionary
	j = {}

	for key in dictionary:
		print("Fetching data for", key)
		resources = dictionary[key]['resources']
		indicator_url = ""
		dictionary_url = ""
		for resource in resources:
			filename = resource.split("/")[-1]	
			if filename.startswith("indicadores"):
				indicator_url = resource
			elif filename.startswith("diccionario"):
				dictionary_url = resource
		try:
			response = urllib.request.urlopen(dictionary_url)
			reader = csv.reader(io.TextIOWrapper(response))
			# Skipping the first three rows. 
			next(reader)
			next(reader)
			next(reader)
			next(reader)
			# Ultra lazy. Need to optimize. Badly.
			for row in reader:
				indicator_id = row[0]
				indicator_name = row[1]
				print("Fetching indicator", indicator_name)
				ring_name = row[2][3:] # Not super-safe
				area_name = row[3][3:] # Not super-safe

				# Building a set of nested dictionaries. Not spatially efficient.
				# Warning: Confusion ahead.
				i = {}
				i['name'] = indicator_name
				ind = get_indicators(url=indicator_url, indicator_id=indicator_id)
				i['values'] = ind
				print(i)
				
				e = {}
				e[indicator_id] = i
				print(e)
				
				r = {}
				r[ring_name] = e
				print(r)
				
				j[key] = r
				
		except TypeError as te:
			print(te)

	with open("data.json", 'w') as fout:
		json.dump(j, fout)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)