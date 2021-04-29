from dnsimple import Client
from dnsimple.struct import ZoneRecordInput
from dnsimple.exceptions import DNSimpleException


# Replace with eRezLife API token
token = "TOKENTOKENTOKENTOKEN"

# Replace with US & CA proxy server IPs
ip_map = {
    "34.231.38.200": "UPDATE-WITH-AWS-US-DNS.com",
    "52.60.69.35": "UPDATE-WITH-AWS-CA-DNS.com",
}


client = Client(sandbox=True, access_token=token)
# client = Client(access_token=token)

account_id = client.identity.whoami().data.account.id
zones = client.zones.list_zones(account_id).data

page = 1
records = client.zones.list_records(account_id, zones[0].name).data

while records:
    for record in records:
        if record.type == "A" and record.content in ip_map:
            print(record.id, record.type, record.name, record.content)
            try:
                client.zones.delete_record(account_id, zones[0].name, record.id)
                client.zones.create_record(
                    account_id,
                    zones[0].name,
                    ZoneRecordInput(
                        type="CNAME", name=record.name, content=ip_map[record.content], ttl=300
                    )
                )
            except DNSimpleException as e:
                print(e.message, e.errors)
    page += 1
    records = client.zones.list_records(account_id, zones[0].name, page=page).data
