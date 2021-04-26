from dnsimple import Client
from dnsimple.struct import ZoneRecordUpdateInput


# Replace with eRezLife API token
token = "TOKENTOKENTOKENTOKEN"

# Replace with US & CA proxy server IPs
ips = ["50.87.234.153"]


# client = Client(sandbox=True, access_token=token)
client = Client(access_token=token)

account_id = client.identity.whoami().data.account.id
zones = client.zones.list_zones(account_id).data

page = 1
records = client.zones.list_records(account_id, zones[0].name).data

while records:
	for record in records:
		if record.type == "A" and record.content in ips:
			print(record.id, record.type, record.name, record.content)
			client.zones.update_record(account_id, zones[0].name, record.id, ZoneRecordUpdateInput(ttl=300))
	page += 1
	records = client.zones.list_records(account_id, zones[0].name, page=page).data
