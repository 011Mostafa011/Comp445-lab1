from sys import argv
import clientclone
import optparse

parser = optparse.OptionParser()
parser.add_option("-v","--verbose",action="store_true", help="Prints the detail of the response such as protocol, status, and headers.", dest="verbose") 
parser.add_option("--h","--header", action="store",type = str, help="Associates headers to HTTP Request with the format 'key:value'",dest="header")
parser.add_option("-d","--sendData",action="store",type="string", help ="Associates an inline data to the body HTTP POST request",dest="data")
parser.add_option("-f","--sendFile",action="store",type=str, help ="Associates the content of a file to the body HTTP POST request",dest="data")
(options,args) = parser.parse_args()


action = argv[1]
url = argv[2]
url = url.split('http://')[1]


client = clientclone.HTTPClient(options,url)

if action =='get':
    client.getHTTP()

elif action == 'post':
    client.postHTTP()

else:
    print("Error use either 'get' or 'post' in argument line")
    exit(1)

client.run_client()



