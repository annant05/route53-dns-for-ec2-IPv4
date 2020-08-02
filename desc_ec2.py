import boto3
from collections import defaultdict
import json 

event_json = json.loads(open("cloudwatchevent.json",'r').read()) 
#key = ''
#secret = ''
instance_id = event_json['detail']['instance-id']
instance_state = event_json['detail']['state']


print(instance_id,instance_state)

aws_session = boto3.Session(
    # aws_access_key_id=config_json["AWS_ACCESS_KEY"],
    # aws_secret_access_key=config_json["AWS_SECRET_KEY"],
    )

ec2_client = aws_session.client ('ec2')

ec2_described =  ec2_client.describe_instances( InstanceIds=['i-031bc1e674943a27d'])
print(ec2_described)

# running_instances = ec2.instances.filter(Filters=[{
#     'Name': 'instance-state-name',
#     'Values': ['running']}])

# ec2info = defaultdict()
# for instance in running_instances:
#     for tag in instance.tags:
#         if 'Name'in tag['Key']:
#             name = tag['Value']
#     # Add instance info to a dictionary         
#     ec2info[instance.id] = {
#         'Name': name,
#         'Type': instance.instance_type,
#         'State': instance.state['Name'],
#         'Private IP': instance.private_ip_address,
#         'Public IP': instance.public_ip_address,
#         'Launch Time': instance.launch_time,
#         'Instance ID': instance.id,
#         'Public DNS': instance.public_dns_name 
#         }

# attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time', 'Instance ID', 'Public DNS']
# for instance_id, instance in ec2info.items():
#     for key in attributes:
#         print("{0}: {1}".format(key, instance[key]))
#     print("------")


# print('Hello')
