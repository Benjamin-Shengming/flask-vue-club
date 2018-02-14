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

export { getBackendAPIURI }
