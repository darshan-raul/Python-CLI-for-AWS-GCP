

from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt, Separator

from examples import custom_style_2

from pyfiglet import Figlet
import boto3

s3 = boto3.client('s3')
iam = boto3.client('iam')
f = Figlet(font='big')

def getbuckets():
    bucketlist=[]
    buckets=s3.list_buckets()
    for i in buckets['Buckets']:
        bucket= i['Name']
        print("> " +bucket)
        bucketlist.append({'name':bucket})
    #print(bucketlist)
    return bucketlist

def getusers():
    users=iam.list_users()
    userlist=[]
    
    for user in users['Users']:
        name=user['UserName']
        print("> "+name)
        userlist.append({"name":name})
    return userlist

def getgroups():
    groups=iam.list_groups()
    grouplist=[]
        
    for group in groups['Groups']:
        name=group['GroupName']
        print("> "+name)
        grouplist.append({"name":name})

    return grouplist

def bucket_list(bucket_choices):
    bucketlist=getbuckets()
    return bucketlist

def user_list(bucket_choices):
    userlist=getusers()
    return userlist

def group_list(bucket_choices):
    grouplist=getgroups()
    return grouplist

def take_action(mainanswers):
    options=[]
    
    if mainanswers['service'] == 'S3':
        if mainanswers['action'] == 'Create Bucket':
            bucket_name=input("What is the name of the bucket you want to create ( Use comma if you want to create multiple buckets): ")###Need to add this functionality later (from mobile app script)
            location=input("In which region do you want to create the bucket")
            s3.create_bucket(Bucket=str(bucket_name), CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
            options.extend(['Create more buckets','Exit'])
        if mainanswers['action'] == 'Delete Bucket':
            print("delete me aa")
            bucket_choices = prompt(bucket_choice, style=custom_style_2)
            pprint(bucket_choices) 
            deletebucket(bucket_choices)
            options.extend(['Delete more buckets','Exit'])
    if mainanswers['service'] == 'IAM':
        if mainanswers['action'] == 'Create User':
            username=input("What is the name of the user you want to create: ")
            print("Creating user")
            iam.create_user( UserName=str(username))
            options.extend(['Create More users','Exit'])
        if mainanswers['action'] == 'Create Group':
            groupname=input("What is the name of the group you want to create: ")
            print("Creating group")
            iam.create_group(GroupName=str(groupname))
            options.extend(['Create More Groups','Exit']) 
        if mainanswers['action'] == 'Delete User':
            print("delete user me aa")
            user_choices = prompt(user_choice, style=custom_style_2)
            pprint(user_choices) 
            deleteuser(user_choices)
            
            #pprint(bucket_choices) 
            #deletebucket(bucket_choices)
            options.extend(['Delete more users','Exit'])
        if mainanswers['action'] == 'Delete Group':
            print("delete group me aa")
            
            options.extend(['Delete more groups','Exit'])   
    return options


def deletebucket(bucket_choices):
    print("deleting bucket")
    bucketname=bucket_choices['bucket'][0]
    s3.delete_bucket(  Bucket=str(bucketname))

def deleteuser(user_choices):
    print("deleting user")
    username=user_choices['user'][0]
    iam.delete_user( UserName=str(username))


def get_service_data(mainanswers):
    options = []
    if mainanswers['service'] == 'S3':
        print("\n #############Buckets############ \n ")
        getbuckets()
        options.extend(['Create Bucket','Delete Bucket','List Bucket Objects','Upload file to Bucket','Go Back'])
        

    
    elif mainanswers['service'] == 'EC2':
        print("\n #############Instances############ \n ")
        options.extend(['Start Instance','Stop Instance','Go Back'])

    elif mainanswers['service'] == 'IAM':
        print("\n #############Users############ \n ")
        getusers()
        print("\n #############Groups############ \n ")
        getgroups()
        options.extend(['Create User','Create Group','Delete User','Delete Group','Go Back'])
             
        
    return options

mainquestions = [
    {
        'type': 'list',
        'name': 'service',
        'message': 'Which AWS service you want to use ?',
        'choices': [
            Separator('---------Compute Services---------'),
            'EC2',
            'Lambda',
            Separator('---------Storage Services---------'),
            'S3',
            'RDS',
            Separator('---------Network Services---------'),
            'Route53',
            'VPC',
            Separator('---------Management Services---------'),
            'IAM',
            'Cloudwatch'

        ]
    },
    {
        'type': 'list',
        'name': 'action',
        'message': "Actions" ,
        'choices': get_service_data
        
    },
    {
        'type': 'list',
        'name': 'delivery',
        'message': 'Which vehicle you want to use for delivery?',
        'choices': take_action
    },
]


bucket_choice=[{
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select Buckets',
        'name': 'bucket',
        #'choices': ['test1','test2'],
        'choices': bucket_list
}
        ]

user_choice=[{
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select Users',
        'name': 'user',
        #'choices': ['test1','test2'],
        'choices': user_list
}
        ]
print (f.renderText('AWS CLI'))
print('A small little CLI to interact with AWS Services')
print('Made with <3 by Darshan Raul \n')
mainanswers = prompt(mainquestions, style=custom_style_2)

pprint(mainanswers)



