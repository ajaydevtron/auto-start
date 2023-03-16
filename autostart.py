import subprocess as sp,sys

username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]
key=sys.argv[4]
val=sys.argv[5]
q1="[?tags.{}==\`{}\`].name".format(key,val)

def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput

#To Check the status of Vm
def checkvmstatus(vmname,rgname):
    vmstatus=sp.getoutput("az vm show -d  --name {}  --resource-group {}  --query powerState -o tsv".format(vmname,rgname))
    return vmstatus
 
#Function to ShutDown Vm 
def shutdown():
    str=sp.getoutput("az vm list --query {} -o tsv".format(q1))
    l=list(str.split())
    #print(l)
    for x in range(len(l)):
        print(f" Details of VM  name:{l[x]} ")
        #To get resource group pf vm
        k="[?name==\`{}\`].resourceGroup".format(l[x])
        
        r=sp.getoutput("az vm list --query {}  -o tsv".format(k))
        
        vmstatus=checkvmstatus(l[x],r)
        print(f"status is :{vmstatus}")
        #stopping vm by checking status
        print("VM starting......")
        if vmstatus=="VM stopped":
            sp.getoutput("az vm start -n {} -g {}".format(l[x],r))
            time.sleep(3)
            print("VM started")
        elif vmstatus=="VM deallocated":
            sp.getoutput("az vm start -n {} -g {}".format(l[x],r))
            time.sleep(3)
            print("VM started")
        else:
            print("Already Running")


authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    shutdown()
else:
    print("Authentication failed",authout[1])
