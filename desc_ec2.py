import boto3
import json

config = json.loads(open("config.json", 'r').read())
event_json = json.loads(open("cloudwatchevent.json", 'r').read())
# key = ''
# secret = ''
# instance_state = event_json['detail']['state']

# print(instance_id, instance_state)

aws_session = boto3.Session(
    region_name=config['AWS_REGION']
    # aws_access_key_id=config_json["AWS_ACCESS_KEY"],
    # aws_secret_access_key=config_json["AWS_SECRET_KEY"],
)


# def lambda_handler(event, context):
#     # TODO implement
#     print(event)
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }


def desc_instance(instance_id):
    ec2_client = aws_session.client('ec2')
    ec2_described = ec2_client.describe_instances(
        InstanceIds=['i-09298412db4b7d4a1'])['Reservations'][0]['Instances'][0]
    print(ec2_described)

    return_info = {}

    instance_state = ec2_described['State']['Name']
    instance_tags = ec2_described['Tags'] or None

    if instance_state == 'running':
        return_info['ipv4'] = ec2_described['PublicIpAddress']
    elif instance_state == 'stopped':
        return_info['ipv4'] = '127.0.0.1'
    elif instance_state == 'terminated':
        return_info['ipv4'] = None

    if instance_tags is not None:
        for tag_elem in instance_tags:
            if (tag_elem['Key']).lower() == 'dns':
                return_info['dns'] = tag_elem['Value']

    return return_info

    def main(instance_id):
        instance_id = event_json['detail']['instance-id']

    # for elem in instance_tags:
    #     if (elem['Key']).lower() == 'dns':
    #         print(elem['Value'])

    print("end")

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
