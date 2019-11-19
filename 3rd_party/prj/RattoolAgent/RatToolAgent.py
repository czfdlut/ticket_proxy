print("test agnet import before==============")
CaptivePortal = __import__("client_auth.WebAuth",fromlist = ['']).__dict__["WebAuth"]
print("CaptivePortal: ", CaptivePortal)
print("test agnet import after==============")
