import boto3
from collections import defaultdict
#key = 'AKIAJ4NOSZX7SWL7IFGQ'
#secret = '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'

ec2 = boto3.resource('ec2')

running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = defaultdict()
for instance in running_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary         
    ec2info[instance.id] = {
        'Name': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': instance.launch_time,
        'Instance ID': instance.id,
        'Public DNS': instance.public_dns_name 
        }

attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time', 'Instance ID', 'Public DNS']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("------")


print('Hello')
