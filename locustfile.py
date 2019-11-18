#!/usr/bin/env python3
from locust import HttpLocust, TaskSet, task
from locust import clients as locustclients
import urllib.parse

import os
import xmltodict
import random
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from dateutil import parser # for parsing iso 8601 formatted date times
from math import floor

# Set environment variable WMS_ACCESS_KEY to
# access WMS servers that require an additional access key.
#
# e.g. WMS_ACCESS_KEY=myauthkey=mysecretaccesstoken
#
# The parameter 'myauthkey' will then be included in all requests

WMS_ACCESSS_KEY = {}
keyvalue = os.getenv('WMS_ACCESS_KEY', None)
if not keyvalue is None:
    parts = keyvalue.split("=")
    WMS_ACCESSS_KEY[parts[0]]=parts[1]

WEIGHT_GET_CAPABILITIES = int(os.getenv('WEIGHT_GET_CAPABILITIES', "1"))
WEIGHT_GET_LEGEND_GRAPHIC = int(os.getenv('WEIGHT_GET_LEGEND_GRAPHIC', "2"))
WEIGHT_GET_MAP = int(os.getenv('WEIGHT_GET_MAP', "10"))

verbose = os.getenv('LOG_VERBOSE', '0')
VERBOSE = False
if verbose.lower() == "1":
    VERBOSE = True

if VERBOSE:
    def vprint(*args, **kwargs):
        print(*args, **kwargs)
else:
    vprint = lambda *a, **k: None # do-nothing function

WMS_VERSION_111 = "1.1.1"
WMS_VERSION_130 = "1.3.0"

WMS_SUPPORTED_VERSIONS = [WMS_VERSION_111, WMS_VERSION_130]

#Allowed MIME TYPEs for WMS Capabilities XML
MIME_TYPES_GET_CAPABILITIES=[
    "application/vnd.ogc.wms_xml",
    "application/xml",
    "text/xml",
]

TIME_FORMAT_ISO8601 = "%Y-%m-%dT%H:%M:%S.%fZ" 

PERIODICITY_PATTERN = re.compile(
     r"^P" 
    +r"((?P<years>\d+)Y)?"
    +r"((?P<months>\d+)M)?"
    +r"((?P<days>\d+)D)?"
    +r"(T"
    +r"((?P<hours>\d+)H)?"
    +r"((?P<minutes>\d+)M)?"
    +r"((?P<seconds>\d+)S)?"
    +r")?$")

def getCommonWMSRequestParams(wmsversion:str):
    commonparams = {
        "service": "wms",
        "version": wmsversion
    }
    commonparams.update(WMS_ACCESSS_KEY) # add access key if environment variable set
    return commonparams

def getPeriodTimedelta(period:str):
    """
    Returns corresponding the timedelta for the time period string.

    See "OpenGIS Web Map Service (WMS) Implementation Specification" 
    at http://portal.opengeospatial.org/files/?artifact_id=14416 
    Chapter "D.3 Period format"

    An ISO 8601 Period is used to indicate the time resolution of the available data. The ISO 8601 format for representing a period of time is used to represent the resolution: Designator P (for Period), number of years Y, months M, days D, time designator T, number of hours H, minutes M, seconds S. Unneeded elements may be omitted.
    
    EXAMPLES:
        P1Y — 1year
        P1M10D — 1 month plus 10 days PT2H — 2 hours
        PT1.5S — 1.5 seconds (this is not yet supported here)
    """
    match = PERIODICITY_PATTERN.match(period)
    if (match is None):
        raise Exception("Invalid time period format found: '{}'.".format(period))
    
    delta = {
        "years": 0,
        "months": 0,
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0
    }
    nonZeroTotalPeriod = False
    for dim in delta.keys():
        if not match.group(dim) is None:
            delta[dim] = int(match.group(dim))
            if (delta[dim] > 0):
                nonZeroTotalPeriod = True
    if nonZeroTotalPeriod is False:
        raise Exception("Invalid time period: '{}'. Period has zero length.".format(period))
    return relativedelta(
        years = delta["years"],
        months = delta["months"],
        days = delta["days"],
        hours = delta["hours"],
        minutes = delta["minutes"],
        seconds = delta["seconds"])




def hasValidGetCapabilitiesResponseType(contentType:str):
    """
    Checks the response 'content-type' string for validity. Returns True if valid, else returns False.
    """
    for mimeType in MIME_TYPES_GET_CAPABILITIES:
        if mimeType in contentType:
            # found valid string
            return True
    return False

def getRandomBoundingBox():
    north = random.randrange(0, 90)
    south = north - 90
    west = random.randrange(-180, 0)
    east = west + 180
    return "%s,%s,%s,%s" % (west, south, east, north)

def getStyles (layer: xmltodict.OrderedDict):
    """
    Returns a list of the available layer styles.
    """
    styles = {}
    if "Style" in layer:
        if type(layer["Style"] ) == list :
            for style in layer["Style"]:
                legendUrl = getLegendURL(style)
                styles[style["Name"]] = { "LegendURL": legendUrl }
                
        else:
            legendUrl = getLegendURL(layer["Style"])
            styles[layer["Style"]["Name"]] = { "LegendURL": legendUrl }
    return styles

def getLegendURL( style: xmltodict.OrderedDict):
    legendUrl = None
    if "LegendURL" in style:
        if "OnlineResource" in style["LegendURL"]:
            if "@xlink:href" in style["LegendURL"]["OnlineResource"]:
                legendUrl = style["LegendURL"]["OnlineResource"]["@xlink:href"]
    return legendUrl


def formatDateTime(ts:datetime):
    """
        Formats the datetime according to D.2.1 of WMS Spec: ccyy-mm-ddThh:mm:ss.sssZ

        A time zone suffix is mandatory if the hours field appears in the time string. 
        All times should be expressed in Coordinated Universal Time (UTC), indicated 
        by the suffix Z (for "zulu"). When a local time applies, a numeric time zone 
        suffix as defined by ISO 8601:2004, 5.3.4.1 shall be used. The absence of any 
        suffix at all means local time in an undefined zone, which shall not be 
        used in the global network of map servers enabled by this International Standard.
    """
    return ts.isoformat(timespec='milliseconds').replace("+00:00","Z")

def enumerateAvailableTimes(text:str):
    """
        Parses the time definition and returns a list of available times,
        
        Example:
        - input: 
            "2019-11-07T09:00:00Z,2019-11-09T21:00:00Z/2019-11-22T21:00:00Z/P1D"
        - output:
          [ "2019-11-07T09:00:00Z",
            "2019-11-09T21:00:00Z",
            "2019-11-09T21:00:00Z",
            "2019-11-10T21:00:00Z",
            "2019-11-11T21:00:00Z",
            ...
            "2019-11-21T21:00:00Z",
            "2019-11-22T21:00:00Z"
          ]

    """
    definitions  = text.split(",")
    values = [] # = { "beginning": None, "end" : None, "step": None }
    for definition in definitions:
        if not "/" in definition:
            # simple time stamp given
            values.append(definition)
            #beginning = datetime.strptime(definition, TIME_FORMAT_ISO8601)
            #values["beginning"] = beginning
            #values["end"] = beginning
        else :
            # a start/end/period definition given
            start, end, period = definition.split("/")
            start = parser.parse(start)
            end = parser.parse(end)
            try:
                delta = getPeriodTimedelta(period=period)
            except:
                raise Exception("Error parsing the step in time definition: '{}'".format(definition))
            while start <= end:
                values.append( formatDateTime(start))
                start = start + delta
            #values["beginning"] = beginning
            #values["end"] = end
            #values["step"] = getPeriodTimedelta(step)
    return values

def getRandomTime(start:datetime, end:datetime, step:relativedelta):
    if start == end:
        return start

    if relativedelta is None:
        if random.randint(0,1) == 0:
            return start
        else:
            return end

    steps = (end.timestamp() - start.timestamp()) / step.total_seconds()
    steps = floor (steps) #make an integer (this should not change the value)
    radomdelta = relativedelta( seconds=step.total_seconds*random.randint(0, steps) )
    return end - radomdelta


def parseDimension(dimension:xmltodict.OrderedDict):
    """
        Parse the dimension/extent defintions (WMS Version 1.1.1/1.3.0)
    """
    try:
        #possible values defined
        dim = {
            "name" : dimension["@name"],
            "values" : dimension["#text"], #possible values
            "default" : dimension["@default"] #default value
        }
    except:
        # no values defined
        dim = {
            "name" : dimension["@name"],
            "values" : dimension["@default"], #fall back to default
            "default" : dimension["@default"] #default value
        }
    
    if dim["name"] == "time":
        times = enumerateAvailableTimes(dim["values"])
        dim["values"] = times

    return dim

def getAllLayers(capabilities:xmltodict.OrderedDict, wmsversion:str):
    """
    Returns all available layers from the capabilities document (as xmltodict dictionary)
    """
    rootNodeName = "WMS_Capabilities"
    if wmsversion == WMS_VERSION_111:
        rootNodeName = "WMT_MS_Capabilities"
    
    root = capabilities[rootNodeName]["Capability"]["Layer"]
    nodes = [ root ]
    flattenedLayers = []
    # traverse the layer tree and
    while len(nodes) > 0:
        parent = nodes.pop()
        if "Layer" in parent:
            # it's a layer group
            # append all sublayers
            if type(parent["Layer"] ) == list :
                for child in parent["Layer"]:
                    nodes.append(child)
            else:
                nodes.append(parent["Layer"])
        else:
            # it's a layer
            flattenedLayers.append(parent)
    
    allLayers = {}
    for layer in flattenedLayers:
        # get the available styles
        styles = getStyles(layer)
        dimensions = getDimensions(layer, wmsversion = wmsversion)

        allLayers[layer["Name"]] = {
            "title": layer["Title"],
            "name": layer["Name"],
            "styles": styles,
            "dimensions": dimensions,
        }
    return allLayers

def getDimensions(layer:xmltodict.OrderedDict, wmsversion:str):
    """
    Parse available dimensions
    """
    ret = {}

    dimension = "Dimension"
    if wmsversion == WMS_VERSION_111:
        dimension = "Extent"

    if not dimension in layer:
        return ret

    dimensions = layer[dimension]
    if type(dimensions) == list:
        # serveral dimensions available
        for dimension in dimensions:
            dim = parseDimension(dimension)
            ret[dim["name"]] = dim
    else:
        # only one dimension available
        dim = parseDimension(dimensions)
        ret[dim["name"]] = dim
    return ret

def getRandomGetMapRequest(allLayers:dict, wmsversion:str):
    """
    Returns GetMap request params for a random layer.

    From all available layers randomly picks a layer, style, bounding box and time dimension (if available).
    """
    randomLayerName = random.choice(list(allLayers.keys()))
    randomLayer = allLayers[randomLayerName]
    randomBbox = getRandomBoundingBox()

    crsparamname = "crs" # WMS 1.3.0
    if (wmsversion == WMS_VERSION_111):
        crsparamname = "srs" # WMS 1.1.1
    

    getMapRequestParams = {
        "request": "GetMap",
        crsparamname: "EPSG:4326",
        "layers": randomLayer["name"],
        "width": 1200,
        "height": 600,
        "format": "image/png",
        "bbox": randomBbox,
    }

    # merge common request params into request
    commonparams = getCommonWMSRequestParams(wmsversion=wmsversion)
    getMapRequestParams.update(commonparams)

    if len(randomLayer["styles"]) > 0:
        randomStyleName = random.choice(list(randomLayer["styles"].keys()))
        getMapRequestParams["styles"] = randomStyleName
    
    dimensions = randomLayer["dimensions"]
    if "time" in dimensions:
        getMapRequestParams["time"] = random.choice(dimensions["time"]["values"])
    
    return getMapRequestParams

def getRandomLegendUrlRequest(allLayers:dict, wmsversion:str):
    """
        Returns request params from the predefined "LegendURL" metadata of a random layer.
    """
    randomLayerName = random.choice(list(allLayers.keys()))
    randomLayer = allLayers[randomLayerName]
    if len(randomLayer["styles"].keys()) < 1:
        return None
    randomStyleName = random.choice(list(randomLayer["styles"].keys()))

    url = randomLayer["styles"][randomStyleName]["LegendURL"]
    url = urllib.parse.unquote(url)
    getLegendGraphicRequest = {
        "url" : url.split("?")[0]
    }
    params = url.split("?")[1].split("&")
    for param in params:
        if "=" in param:
            keyvalue = param.split("=")
            getLegendGraphicRequest[keyvalue[0]] = keyvalue[1]
        else:
            getLegendGraphicRequest[keyvalue] = ""

    # HACK: hack for invalid LegendUrls in skinnywms
    if not "height" in getLegendGraphicRequest.keys() or getLegendGraphicRequest["height"] == "":
        getLegendGraphicRequest["height"] = 20
    if not "width" in getLegendGraphicRequest.keys() or getLegendGraphicRequest["width"] == "":
        getLegendGraphicRequest["width"] = 20
    #print("LegendURL: {}\n  Request Params: {}\n".format(url, getLegendGraphicRequest))
    return getLegendGraphicRequest

def getRandomGetLegendGraphicRequest(allLayers:dict, wmsversion:str):
    """
    Returns GetMap request params for a random layer.

    From all available layers randomly picks a layer, style, bounding box and time dimension (if available).
    """
    randomLayerName = random.choice(list(allLayers.keys()))
    randomLayer = allLayers[randomLayerName]

    getLegendGraphicRequestParams = {
        "service": "wms",
        "version": wmsversion,
        "request": "GetLegendGraphic",
        "layer": randomLayer["name"],
        "width": 20,
        "height": 20,
        "format": "image/png",
    }

    # merge common request params into request
    commonparams = getCommonWMSRequestParams(wmsversion=wmsversion)
    getLegendGraphicRequestParams.update(commonparams)

    if len(randomLayer["styles"].keys()) > 0:
        randomStyleName = random.choice(list(randomLayer["styles"].keys()))
        getLegendGraphicRequestParams["style"] = randomStyleName
    else:
        return None
    
    return getLegendGraphicRequestParams

def getGetCapabilitiesRequest(wmsversion:str):
    getCapabilitiesRequestParams = {
        "request": "GetCapabilities",
    }

    # merge common request params into request
    commonparams = getCommonWMSRequestParams(wmsversion=wmsversion)
    getCapabilitiesRequestParams.update(commonparams)

    return getCapabilitiesRequestParams

def sendGetCapabilitiesRequest(client:locustclients.HttpSession, wmsversion:str):
    params = getGetCapabilitiesRequest(wmsversion=wmsversion)

    with client.request("GET", "", params=params, name="WMS-{}-GetCapabilities".format(wmsversion), catch_response=True ) as response:
        url = urllib.parse.unquote(response.url)
        if not response.status_code == 200:
            errormsg = "Request failed with HTTP status code: '{}'\n Request URL: {}\n Response-Content: '{}'".format(response.status_code, url, response.content )
            vprint( "Request failed:\n{}".format(errormsg) )
            response.failure(errormsg)
            return
        
        if not hasValidGetCapabilitiesResponseType(response.headers['content-type']):
            response.failure("Wrong response content-type encountered: '%s' (see %s)" % (response.headers['content-type'], "https://cite.opengeospatial.org/teamengine/about/wms/1.1.1/site/OGCTestData/wms/1.1.1/spec/wms1.1.1.html#basic_elements.params.format"))
            return
        
        if response.content == "":
            response.failure("No data")
            return
        
        try:
            capabilities = xmltodict.parse(response.content)
            #vprint("Request successful: {}".format(url))
            return capabilities
        except:
            response.failure("Failed to parse GetCapabilities XML")
            return

def sendGetMapRequest(client:locustclients.HttpSession, params:dict, wmsversion:str):
    with client.request("GET", "", params=params, name="WMS-{}-GetMap".format(wmsversion), catch_response=True ) as response:
        if response.status_code == 200:
            url = urllib.parse.unquote(response.url)
            if response.headers['content-type'] != "image/png":
                errormsg = "Expected format 'image/png' but got '{}' instead\n Request URL: {}\n Request params: '{}'\nResponse: '{}'\n".format(response.headers['content-type'], url, params, response.text)
                vprint( "Request failed:\n{}".format(errormsg) )
                response.failure(errormsg)
            else:
                #vprint("Request successful: {}".format(url))
                response.success()


def sendGetLegendGraphicRequest(client:locustclients.HttpSession, params:dict, wmsversion:str):
    requestUrl = ""
    if "url" in params:
        # extract request url from params
        requestUrl = params["url"]
        params.pop("url")

    with client.request("GET", requestUrl, params=params, name="WMS-{}-GetLegendGraphic".format(wmsversion), catch_response=True ) as response:
        #if response.history:
        #    #Response was redirected
        #    for resp in response.history:
        #        print("Redirected with code '{}' to url '{}'".format(resp.status_code,resp.url))
        if response.status_code == 200:
            url = urllib.parse.unquote(response.url)
            if response.headers['content-type'] != "image/png":
                errormsg = "Expected format 'image/png' but got '{}' instead\n Request URL: {}\n Request params: '{}'\nResponse: '{}'\n".format(response.headers['content-type'], url, params, response.text) 
                vprint( "Request failed:\n{}".format(errormsg) )
                response.failure(errormsg)
            else:
                #vprint("Request successful: {}".format(url))
                response.success()

class WebsiteTasks(TaskSet):
    """
        This task simulates users using different WMS versions and
        acessing the startpage "/" as well as sending GetCapabilites
        and GetMap requests.
    """

    allLayers = {
    }

    #@task(2)
    #def index(self):
    #    self.client.get("/")

    @task(WEIGHT_GET_CAPABILITIES)
    def get_capa(self):
        wmsversion = random.choice(WMS_SUPPORTED_VERSIONS)
        capabilities = sendGetCapabilitiesRequest(client=self.client, wmsversion=wmsversion)

        if capabilities is None:
            return
        
        if not wmsversion in self.allLayers:
            # parse the capabilities document once
            # for each WMS version
            self.allLayers[wmsversion] = getAllLayers(capabilities=capabilities, wmsversion=wmsversion)

    @task(WEIGHT_GET_LEGEND_GRAPHIC)
    def get_legend_graphic(self):
        wmsversion = random.choice(WMS_SUPPORTED_VERSIONS)
        if not wmsversion in self.allLayers:
            # Get Capabilities document not (yet) processed
            return
        
        #getLegendGraphicRequest = getRandomGetLegendGraphicRequest(self.allLayers[wmsversion], wmsversion=wmsversion)
        getLegendGraphicRequest = getRandomLegendUrlRequest(self.allLayers[wmsversion], wmsversion=wmsversion)

        if not getLegendGraphicRequest is None:
            sendGetLegendGraphicRequest(client=self.client, params=getLegendGraphicRequest, wmsversion=wmsversion)

    @task(WEIGHT_GET_MAP)
    def get_map(self):
        wmsversion = random.choice(WMS_SUPPORTED_VERSIONS)
        if not wmsversion in self.allLayers:
            # Get Capabilities document not (yet) processed
            return
        getMapRequest = getRandomGetMapRequest(self.allLayers[wmsversion], wmsversion=wmsversion)
        sendGetMapRequest(client=self.client, params=getMapRequest, wmsversion=wmsversion)



class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000


if __name__ == "__main__":
    currentPath = os.path.dirname(os.path.realpath(__file__))
    for provider in ["dwd", "hh"]:
        print("Test for Provider: {}".format(provider))
        for wmsversion in WMS_SUPPORTED_VERSIONS:
            capabilities = None
            with open("{}/testdata/getcapabilities_{}_{}.xml".format(currentPath,wmsversion, provider), "r",1024, "utf-8") as stream:
                capabilities = xmltodict.parse(stream.read())
            
            allLayers = { 
                wmsversion : getAllLayers(capabilities=capabilities, wmsversion=wmsversion) 
            }
            getMapRequest = getRandomGetMapRequest(allLayers[wmsversion], wmsversion=wmsversion)
            print ("{}-WMS-{}-GetMap-Request: \n{}\n".format(provider, wmsversion,getMapRequest))
            getLegendGraphicRequest = getRandomGetLegendGraphicRequest(allLayers[wmsversion], wmsversion=wmsversion)
            print ("{}-WMS-{}-GetLegendGraphic-Request: \n{}\n".format(provider, wmsversion,getLegendGraphicRequest))
            getLegendURLRequest = (getRandomLegendUrlRequest(allLayers[wmsversion], wmsversion=wmsversion))
            print ("{}-WMS-{}-GetLegendGraphic-Request-From_LegendURL: \n{}\n".format(provider, wmsversion,getLegendURLRequest))
