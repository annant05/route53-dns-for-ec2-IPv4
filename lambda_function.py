import boto3
import json


config = json.loads(open("config.json", 'r').read())


# Global Variables
DOMAIN_NAME = config['DOMAIN_NAME']
ROUTE53_ZONE_ID = config['ROUTE53_ZONE_ID']

aws_session = boto3.Session(
    region_name=config['AWS_REGION']
    # aws_access_key_id=config_json["AWS_ACCESS_KEY"],
    # aws_secret_access_key=config_json["AWS_SECRET_KEY"],
)


def lambda_handler(event, context):
    print(event)
    main(event)
    return {
        'statusCode': 200,
        'body': json.dumps(f'Function executed')
    }



def desc_instance(instance_id):
    ec2_client = aws_session.client('ec2')
    ec2_described = ec2_client.describe_instances(
        InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    # print(ec2_described)

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
                return_info['dns'] = ((tag_elem['Value']).lower()).strip()

    return return_info


def delete_route53_record_set(dns):
    route53_client = aws_session.client('route53')

    record_desc = route53_client.list_resource_record_sets(
        HostedZoneId=ROUTE53_ZONE_ID,
        StartRecordName=f'{dns}.{DOMAIN_NAME}',
        StartRecordType='A',
        MaxItems='1'
    )

    record_desc = record_desc['ResourceRecordSets'][0]
    if record_desc['Name'] != f'{dns}.{DOMAIN_NAME}.':
        print(f'records from list {record_desc["Name"]} !=  passed dns: {dns}.{DOMAIN_NAME}.')
        return False

    delete_res = route53_client.change_resource_record_sets(
        HostedZoneId=ROUTE53_ZONE_ID,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': record_desc['Name'],
                        'ResourceRecords': [
                            {
                                'Value': record_desc['ResourceRecords'][0]['Value'],
                            }
                        ],
                        'TTL': record_desc['TTL'],
                        'Type': record_desc['Type'],
                    },
                },
            ],
        },
    )

    print("Deleted record Set", delete_res)
    return True


def create_route53_record_set(ipv4, dns, instance_id):
    if ipv4 is None:
        delete_route53_record_set(dns)
        return False

    route53_client = aws_session.client('route53')

    response = route53_client.change_resource_record_sets(
        HostedZoneId=ROUTE53_ZONE_ID,
        ChangeBatch={
            'Comment': f'DNS attached to instance {instance_id}',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': f'{dns}.{DOMAIN_NAME}',
                        'ResourceRecords': [
                            {
                                'Value': ipv4,
                            },
                        ],
                        'TTL': 300,
                        'Type': 'A',
                    },
                },
            ],
        },
    )
    print("Created record Set", response)
    return True


def main(event_json):
    print("Function START")
    instance_id = event_json['detail']['instance-id']
    instance_meta = desc_instance(instance_id)
    create_route53_record_set(instance_meta['ipv4'], instance_meta['dns'], instance_id)
    print("Function END")
