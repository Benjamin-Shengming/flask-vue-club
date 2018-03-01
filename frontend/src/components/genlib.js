import URI from 'urijs'

function getBackendAPIURI (currentRef, path) {
  console.log('getBackendapiuri')
  console.log(currentRef)
  let fullPath = URI(currentRef)
  console.log(fullPath.origin().toString())
  console.log(fullPath.port().toString())
  let apiURI = fullPath.origin().toString().replace(fullPath.port().toString(), '5000') + path
  console.log('api uri')
  console.log(apiURI)
  return apiURI
}

function prefixAPIURIPath(path) {
  let prefix = '/api_v1';
  return prefix + path;
}

function prefixClubName(clubName, path) {
  return "/" + clubName + path;
}

function prefixFileStore(path) {
  return "/filestore" + path;
}

function prefixService(path) {
  return "/service" + path;
}

function getServiceFileStorePath(clubName, serviceId) {
  return prefixAPIURIPath(
              prefixFileStore(
                prefixClubName(clubName,
                  prefixService("/" + serviceId))))
}

function getServiceMajorPic(href, clubName, item) {
  let url = prefixAPIURIPath(prefixFileStore(
                            prefixClubName(clubName,
                                prefixService("/" + item.id + "/" + item.major_pic)
                        )))
  url = getBackendAPIURI(href, url);
  console.log(url)
  return url;
}

export { getBackendAPIURI,
         prefixAPIURIPath,
         prefixClubName,
         prefixFileStore,
         prefixService,
         getServiceFileStorePath,
         getServiceMajorPic
}
