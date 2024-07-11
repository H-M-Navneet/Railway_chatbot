import requests

url = "https://irctc1.p.rapidapi.com/api/v1/searchStation"

querystring = {"query":"BJU"}

headers = {
	"X-RapidAPI-Key": "4350e08837msh60baa4e99868ec4p157cadjsn64bd696ef316",
	"X-RapidAPI-Host": "irctc1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())